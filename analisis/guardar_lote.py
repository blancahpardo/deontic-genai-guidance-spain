"""Guarda un lote anotado: lee de stdin solo las unidades con DIR=1
(unidad;1;FUERZA;DEST;AMBITO) y marca el resto del lote como DIR=0."""
import sys
n=sys.argv[1]
lab={l.split(';')[0]:l.strip() for l in sys.stdin if l.strip()}
ids=[l.split(' ')[0] for l in open(f'lotes/lote_{n}.txt')]
bad=[k for k in lab if k not in ids]
assert not bad, f'ids fuera del lote: {bad}'
with open(f'anot/lote_{n}.csv','w') as f:
    for i in ids: f.write(lab.get(i,f"{i};0;;;")+'\n')
print(n, len(ids), 'unidades,', len(lab), 'directivas')
