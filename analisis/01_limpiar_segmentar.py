"""Limpieza y segmentación del corpus de guías de IA de universidades españolas.

Entrada: corpus/txt/<archivo>.txt (texto extraído de PDF o HTML) + corpus/inventario.csv
Salida:  analisis/unidades.csv  (una fila por unidad: oración o elemento de lista)
         analisis/docs_limpios/<id>.txt

Unidad de análisis: oración ortográfica o elemento de lista. Cada unidad conserva
el último encabezado visto (contexto), necesario porque muchas guías transfieren la
fuerza deóntica a los epígrafes («Usos no permitidos») y dejan los elementos de la
lista sin verbo modal.
"""
import csv, re, os, collections
import spacy

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXT = os.path.join(BASE, 'corpus', 'txt')
OUT = os.path.join(BASE, 'analisis')
os.makedirs(os.path.join(OUT, 'docs_limpios'), exist_ok=True)

nlp = spacy.load('es_core_news_md', disable=['ner'])
nlp.max_length = 3_000_000

BOILER = re.compile(r'^(Botones de cabecera|banners|UMA|SERVICIO CENTRAL DE INFORMÁTICA|beforecontenttitle|'
                    r'Después del título del contenido|Antes del cuerpo del contenido|Trozos html editables|'
                    r'Menú destacado|Barra lateral derecha|CONFIGURAR .*|SOLICITUDES|INCIDENCIA .*|NORMATIVAS DE USO|'
                    r'PREGUNTAS FRECUENTES|Compartir.*|drag|Home|Inteligencia Artificial|Volver|Arriba)$')
PAGE = re.compile(r'^(p[áa]g\.?\s*\d+(\s*de\s*\d+)?|\d{1,3}|página \d+.*|\d+\s*/\s*\d+)$', re.I)
BULLET = re.compile(r'^\s*([•●▪■◦▶►✓✔✗✘\-–—*]|\d{1,2}[.)]|[a-z][.)])\s+')


def web_trim(doc_id, lines):
    """Recorta cabeceras y pies de las páginas web."""
    if doc_id == 'D23':  # UMA: los capítulos van concatenados; el cuerpo empieza en «Capítulo 0X»
        out, keep = [], False
        for l in lines:
            if l.startswith('Capítulo 0'):
                keep = True; continue
            if l.startswith('Menú destacado'):
                keep = False
            if keep:
                out.append(l)
        return out
    return lines


def clean_lines(doc_id, text):
    # guiones blandos (U+00AD) del maquetado: se eliminan (dentro de línea) o se unen (a final de línea)
    text = text.replace('\xa0', ' ').replace('\xad ', '')
    lines = [l.strip() for l in text.split('\n')]
    lines = [l for l in lines if l]
    lines = web_trim(doc_id, lines)
    lines = [l for l in lines if not BOILER.match(l) and not PAGE.match(l)]
    # líneas repetidas (cabeceras/pies de página o capas duplicadas en PDF): se conserva la primera
    cnt = collections.Counter(lines)
    seen, out = set(), []
    for l in lines:
        if cnt[l] >= 3 or (cnt[l] >= 2 and len(l.split()) >= 4):
            if l in seen:
                continue
            seen.add(l)
        out.append(l)
    return out


def rebuild_paragraphs(lines):
    """Une líneas partidas por el maquetado; separa elementos de lista y encabezados."""
    blocks = []  # (tipo, texto)
    buf = ''
    def flush():
        nonlocal buf
        if buf.strip():
            blocks.append(('p', buf.strip()))
        buf = ''
    for i, l in enumerate(lines):
        is_bullet = bool(BULLET.match(l))
        words = l.split()
        nxt = lines[i + 1] if i + 1 < len(lines) else ''
        # un renglón corto sin puntuación final es encabezado solo si lo que sigue no lo continúa
        # (en maquetaciones a columna estrecha, el primer renglón de una oración también es corto)
        continues = bool(nxt) and (nxt[:1].islower() or (nxt[:1].isdigit() and not BULLET.match(nxt)))
        short_no_stop = (len(words) <= 10 and not re.search(r'[.:;?!»)"]$', l)
                         and (l.isupper() or not continues))
        if is_bullet:
            flush(); buf = BULLET.sub('', l, count=1); continue
        if buf.endswith('\xad'):
            buf = buf[:-1] + l; continue
        if buf.endswith('-') and l[:1].islower():
            buf = buf[:-1] + l; continue
        if short_no_stop and (not buf or re.search(r'[.:;?!]$', buf)):
            flush(); blocks.append(('h', l)); continue
        if buf and re.search(r'[.?!]$', buf) and l[:1].isupper():
            flush(); buf = l; continue
        buf = (buf + ' ' + l) if buf else l
    flush()
    return blocks


def main():
    inv = list(csv.DictReader(open(os.path.join(BASE, 'corpus', 'inventario.csv'), encoding='utf-8')))
    rows = []
    for d in inv:
        text = open(os.path.join(TXT, d['archivo'] + '.txt'), encoding='utf-8').read()
        lines = clean_lines(d['id'], text)
        blocks = rebuild_paragraphs(lines)
        heading = ''
        n = 0
        with open(os.path.join(OUT, 'docs_limpios', d['id'] + '.txt'), 'w', encoding='utf-8') as f:
            for kind, b in blocks:
                f.write(('## ' if kind == 'h' else '') + b + '\n')
        for kind, b in blocks:
            if kind == 'h':
                heading = b
                n += 1
                rows.append(dict(doc=d['id'], unidad=f"{d['id']}-{n:04d}", tipo='encabezado', encabezado=heading, texto=b))
                continue
            for s in nlp(b).sents:
                st = s.text.strip()
                if len(st.split()) < 2:
                    continue
                n += 1
                rows.append(dict(doc=d['id'], unidad=f"{d['id']}-{n:04d}", tipo='oracion', encabezado=heading, texto=st))
    with open(os.path.join(OUT, 'unidades.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['doc', 'unidad', 'tipo', 'encabezado', 'texto'])
        w.writeheader(); w.writerows(rows)
    c = collections.Counter((r['doc'], r['tipo']) for r in rows)
    words = collections.Counter()
    for r in rows:
        if r['tipo'] == 'oracion':
            words[r['doc']] += len(r['texto'].split())
    for d in inv:
        print(d['id'], d['archivo'][:22].ljust(22), 'oraciones', c[(d['id'], 'oracion')], 'encabezados', c[(d['id'], 'encabezado')], 'palabras', words[d['id']])
    print('TOTAL oraciones', sum(v for (k, t), v in c.items() if t == 'oracion'), 'palabras', sum(words.values()))


if __name__ == '__main__':
    main()
