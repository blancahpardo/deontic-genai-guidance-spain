"""Extracción de PDF por bloques con orden de lectura por columnas (PyMuPDF).
Sustituye a la extracción línea a línea de pdfplumber, que mezclaba columnas."""
import pymupdf, csv, os, re
BASE=os.path.dirname(os.path.abspath(__file__))
def page_blocks(p):
    bl=[b for b in p.get_text('blocks') if b[6]==0 and b[4].strip()]
    if not bl: return []
    w=p.rect.width
    xs=sorted(set(round(b[0]) for b in bl))
    # cortes de columna: huecos grandes entre x0 ordenados con bloques a ambos lados
    cols=[[]]
    bl_sorted=sorted(bl,key=lambda b:b[0])
    last=None
    for b in bl_sorted:
        if last is not None and b[0]-last>0.22*w:
            cols.append([])
        cols[-1].append(b); last=b[0]
    out=[]
    for c in cols:
        for b in sorted(c,key=lambda b:(round(b[1]),b[0])):
            t=re.sub(r'\s*\n\s*',' ',b[4]).strip()
            out.append(t)
    return out
inv=list(csv.DictReader(open(os.path.join(BASE,'inventario.csv'),encoding='utf-8')))
for d in inv:
    if d['formato']!='PDF': continue
    doc=pymupdf.open(os.path.join(BASE,'raw',d['archivo']+'.pdf'))
    lines=[]
    for p in doc: lines+=page_blocks(p)
    open(os.path.join(BASE,'txt',d['archivo']+'.txt'),'w',encoding='utf-8').write('\n'.join(lines))
    print(d['id'],d['archivo'],len(' '.join(lines).split()))
