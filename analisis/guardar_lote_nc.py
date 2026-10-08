"""Guarda un lote de no candidatas: lee por stdin las directivas («unidad;FUERZA;DEST;ÁMBITO»),
el resto de unidades del lote queda con DIR = 0. Uso: python guardar_lote_nc.py 27 < pos.txt"""
import sys
n=sys.argv[1]
ids=[l.split('|')[0] for l in open(f'lotes/lote_{n}.txt',encoding='utf-8')]
pos={}
for l in sys.stdin:
    l=l.strip()
    if l: u,F,D,A=l.split(';'); pos[u]=(F,D,A)
bad=[u for u in pos if u not in ids]
assert not bad, f'unidades fuera del lote: {bad}'
V={'F':{'OBL','PROH','PERM','REC','COMP'},'D':{'EST','DOC','INV','COM','INST','NE'},'A':{'INTEG','TRANSP','DATOS','VERIF','DOCEN','APREND','HERRAM','ETICA','OTRO'}}
for u,(F,D,A) in pos.items(): assert F in V['F'] and D in V['D'] and A in V['A'], (u,F,D,A)
with open(f'anot/lote_{n}.csv','w',encoding='utf-8') as f:
    for u in ids: f.write(f'{u};1;{";".join(pos[u])}\n' if u in pos else f'{u};0;;;\n')
print(f'lote {n}: {len(ids)} unidades, {len(pos)} directivas')
