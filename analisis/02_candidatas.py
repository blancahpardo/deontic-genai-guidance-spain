"""Detección de unidades candidatas a contener un acto directivo (o compromisivo).

Filtro de alta cobertura: marca toda unidad (oración, elemento de lista o encabezado)
que contenga al menos una marca formal de modalidad deóntica o de fuerza directiva.
La decisión final (¿es directiva?, ¿qué fuerza?, ¿a quién se dirige?) se toma en la
anotación posterior; aquí solo se identifican las formas.

Categorías de forma (FORM):
  MOD   verbo modal: deber, poder, tener que, haber de, hay que
  PRED  predicado evaluativo/deóntico: es necesario/recomendable/importante… + inf/que; conviene
  PERF  verbo realizativo o de enunciación directiva: recomendar, aconsejar, sugerir, animar,
        alentar, invitar, instar, exigir, requerir, pedir, rogar, prohibir, permitir, autorizar
  PART  participio o adjetivo de estatus: permitido, prohibido, autorizado, obligatorio
  IMP   imperativo (tú/vosotros) o subjuntivo exhortativo en posición inicial (usted, nosotros)
  EVIT  verbo evitar
  SANC  calificación sancionadora: se considerará / constituye / será (considerado) plagio, fraude…
  COMP  compromiso institucional: la universidad (se compromete a | promoverá | garantizará…)
  HEAD  encabezado de lista con léxico deóntico (el elemento hereda la fuerza del epígrafe)
"""
import csv, os, re, collections
import spacy

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'analisis')
nlp = spacy.load('es_core_news_md', disable=['ner'])

PRED_ADJ = r'(necesari[oa]s?|imprescindibles?|obligatori[oa]s?|preceptiv[oa]s?|recomendables?|aconsejables?|convenientes?|importantes?|fundamentales?|esencial(es)?|crucial(es)?|clave|vital(es)?|indispensables?|deseables?|preferibles?|oportun[oa]s?|primordial(es)?|necesidad)'
RE_PRED = re.compile(r'\b(es|son|será|serán|sería|resulta|resultan|resultará|parece|se hace|se considera)\s+(muy\s+|especialmente\s+|altamente\s+|absolutamente\s+|igualmente\s+|por tanto\s+)?' + PRED_ADJ + r'\b', re.I)
RE_PRED2 = re.compile(r'\b(conviene|convendría|hace falta|urge|se hace necesario|es de vital importancia)\b', re.I)
PERF_LEMMAS = {'recomendar', 'aconsejar', 'sugerir', 'animar', 'alentar', 'invitar', 'instar', 'exigir',
               'requerir', 'pedir', 'rogar', 'prohibir', 'permitir', 'autorizar', 'desaconsejar', 'obligar',
               'insistir', 'solicitar', 'encarecer'}
RE_PART = re.compile(r'\b(no\s+)?(est[áa]n?|queda[n]?|será[n]?|se considera[n]?)?\s*(permitid[oa]s?|prohibid[oa]s?|autorizad[oa]s?|vetad[oa]s?|obligatori[oa]s?)\b', re.I)
RE_SANC = re.compile(r'\b(se consider(a|ará|arán|an)|constituy(e|en|e un)|ser[áa]n? considerad[oa]s?|podr[áa] considerarse|puede considerarse|se tratar[áa])\b.{0,40}\b(plagio|fraude|falta|infracci[óo]n|mala pr[áa]ctica|deshonestidad|conducta)', re.I)
RE_COMP = re.compile(r'\b(la universidad|la [A-Z]{2,6}|[A-Z]{3,6}|la instituci[óo]n|nuestra universidad|la comunidad universitaria)\b.{0,40}\b(se compromete|promover[áa]|garantizar[áa]|velar[áa]|impulsar[áa]|facilitar[áa]|ofrecer[áa]|fomentar[áa]|apuesta por|asume)\b', re.I)
RE_HAYQUE = re.compile(r'\bhay que\b|\bhabr[áa] que\b|\btiene[ns]? que\b|\btendr[áa]n? que\b|\bha[ns]? de\b|\bhabr[áa]n? de\b|\bhabrían? de\b|\btendrían? que\b|\btienes que\b', re.I)
RE_HEAD_DEONT = re.compile(r'(compromis|permitid|prohibid|no permitid|recomend|consejo|pautas?|buenas pr[áa]cticas|qu[ée] (se puede|no|hacer|debes|evitar)|usos? (no )?(adecuad|inadecuad|aceptable|responsable|permitid|prohibid|leg[íi]tim|il[íi]cit)|debes|evita|se puede|no se puede|obligaci|requisit|directrices|normas|reglas|principios|l[íi]mites|advertencias|precauciones|do\'?s|sí\b|no\b)', re.I)


def marks(unit_text, heading):
    doc = nlp(unit_text)
    m = set()
    for i, t in enumerate(doc):
        lem = t.lemma_.lower()
        mood = t.morph.get('Mood')
        person = t.morph.get('Person')
        number = t.morph.get('Number')
        if lem in ('deber', 'poder') and t.pos_ in ('AUX', 'VERB'):
            m.add('MOD')
        if lem in PERF_LEMMAS and t.pos_ in ('VERB', 'AUX'):
            m.add('PERF')
        if lem == 'evitar':
            m.add('EVIT')
        if 'Imp' in mood and t.pos_ in ('VERB', 'AUX'):
            m.add('IMP')
        # subjuntivo exhortativo al inicio de oración (usted, nosotros) o negativo de 2.ª persona
        if 'Sub' in mood and t.pos_ in ('VERB', 'AUX'):
            first = [x for x in doc if not x.is_punct][:3]
            if t in first and (('1' in person and 'Plur' in number) or '3' in person or '2' in person):
                m.add('IMP')
            if i > 0 and doc[i - 1].lower_ == 'no' and '2' in person:
                m.add('IMP')
    # imperativo de tú homónimo del presente de 3.ª persona («Verifica la información»):
    # verbo inicial en presente de 3.ª del singular sin sujeto expreso
    toks = [x for x in doc if not x.is_punct and not x.is_space]
    if toks:
        v = toks[0] if toks[0].lower_ != 'no' or len(toks) < 2 else toks[1]
        if v.pos_ in ('VERB', 'AUX') and v.lemma_.lower() not in ('ser', 'haber', 'estar', 'existir', 'tratar', 'parecer', 'resultar') and ('Imp' in v.morph.get('Mood') or (
                'Pres' in v.morph.get('Tense') and '3' in v.morph.get('Person')
                and 'Sing' in v.morph.get('Number') and not any(c.dep_.startswith('nsubj') for c in v.children))):
            m.add('IMP')
    # respaldo: spaCy analiza mal el imperativo en mayúscula inicial («Evita», «Lee», «Sé»);
    # se vuelve a analizar la oración con la inicial en minúscula
    st = unit_text.lstrip(' ¡¿"«(-•●>')
    if st[:1].isupper() and not st[:2].isupper():
        doc2 = nlp(st[:1].lower() + st[1:])
        t2 = [x for x in doc2 if not x.is_punct and not x.is_space]
        if t2:
            v = t2[1] if t2[0].lower_ == 'no' and len(t2) > 1 else t2[0]
            if v.pos_ in ('VERB', 'AUX') and (
                    'Imp' in v.morph.get('Mood')
                    or (t2[0].lower_ == 'no' and '2' in v.morph.get('Person'))
                    or (v.lemma_.lower() not in ('ser', 'haber', 'estar', 'existir', 'tratar', 'parecer', 'resultar')
                        and 'Pres' in v.morph.get('Tense') and '3' in v.morph.get('Person')
                        and 'Sing' in v.morph.get('Number') and not any(c.dep_.startswith('nsubj') for c in v.children))):
                m.add('IMP')
    if re.match(r'^\W*(sé|sed|no seas|no seáis)\s', unit_text, re.I):
        m.add('IMP')
    if re.search(r'\bevit(a|e|en|ad|emos|ar|ando|arse|a[rn]?se)\b', unit_text, re.I):
        m.add('EVIT')
    txt = unit_text
    if RE_PRED.search(txt) or RE_PRED2.search(txt):
        m.add('PRED')
    if RE_PART.search(txt):
        m.add('PART')
    if RE_SANC.search(txt):
        m.add('SANC')
    if RE_COMP.search(txt):
        m.add('COMP')
    if RE_HAYQUE.search(txt):
        m.add('MOD')
    return m


def main():
    rows = list(csv.DictReader(open(os.path.join(OUT, 'unidades.csv'), encoding='utf-8')))
    out = []
    for r in rows:
        m = marks(r['texto'], r['encabezado'])
        head_deont = bool(RE_HEAD_DEONT.search(r['encabezado'] or '')) and r['tipo'] == 'oracion'
        # un elemento sin marcas propias bajo un epígrafe deóntico se marca como HEAD
        if head_deont and not m and len(r['texto'].split()) <= 40:
            m.add('HEAD')
        r['marcas'] = '|'.join(sorted(m))
        r['candidata'] = 'si' if m else 'no'
        out.append(r)
    with open(os.path.join(OUT, 'unidades_marcadas.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)
    c = collections.Counter(r['candidata'] for r in out)
    cm = collections.Counter(x for r in out for x in r['marcas'].split('|') if x)
    print(c, cm)


if __name__ == '__main__':
    main()
