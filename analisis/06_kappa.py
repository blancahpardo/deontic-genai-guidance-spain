"""Calcula el acuerdo entre la anotación asistida por el modelo y la anotación experta (muestra ciega)."""
import pandas as pd, glob, sys
from sklearn.metrics import cohen_kappa_score
# uso: 06_kappa.py [excel anotado] [clave]; por defecto, la muestra de la ronda 2
XLS=sys.argv[1] if len(sys.argv)>1 else 'validacion/muestra_validacion_ronda2_BHP.xlsx'
KEY=sys.argv[2] if len(sys.argv)>2 else 'validacion/clave_muestra.csv'
h=pd.read_excel(XLS,sheet_name='Anotacion',dtype=str).fillna('')
h=h.rename(columns={'DIR':'DIR_h','FUERZA':'FUERZA_h','DEST':'DEST_h','AMBITO':'AMBITO_h'})[['unidad','DIR_h','FUERZA_h','DEST_h','AMBITO_h']]
for c in ['DIR_h','FUERZA_h','DEST_h','AMBITO_h']: h[c]=h[c].str.strip().str.upper()
h['DIR_h']=h['DIR_h'].str.replace('.0','',regex=False)
# etiquetas del modelo: todos los lotes (incluido el lote 25); la última anotación de cada unidad prevalece
rows={}
for f in sorted(glob.glob('analisis/anot/lote_*.csv')):
    if 'muestra' in f: continue  # etiquetas de la experta, no del modelo
    for line in open(f,encoding='utf-8'):
        q=line.rstrip('\n').split(';')
        if len(q)>=5: rows[q[0]]=dict(unidad=q[0],DIR=q[1],FUERZA=q[2],DEST=q[3],AMBITO=q[4])
m=pd.DataFrame(rows.values())
k=pd.read_csv(KEY,dtype=str)
x=h.merge(k,on='unidad').merge(m,on='unidad',how='left')
# unidad que el modelo no anotó (descartada por el filtro) = no directiva
x[['DIR','FUERZA','DEST','AMBITO']]=x[['DIR','FUERZA','DEST','AMBITO']].fillna('')
x['DIR']=x['DIR'].replace('', '0')
done=x[x.DIR_h!='']
print('Unidades anotadas por la experta:',len(done),'de',len(x))
if len(done)==0:
    raise SystemExit('Todavía no hay ninguna fila anotada en la columna DIR.')
bad=done[~done.DIR_h.isin(['0','1'])]
if len(bad): raise SystemExit(f'Hay {len(bad)} filas con un valor de DIR distinto de 0 o 1 (n.º de unidad: {list(bad.unidad)[:10]}).')
print('Filas con DIR = 1 pero sin FUERZA, DEST o AMBITO:', int(((done.DIR_h=='1')&((done.FUERZA_h=='')|(done.DEST_h=='')|(done.AMBITO_h==''))).sum()))
print('DIR: kappa = %.3f' % cohen_kappa_score(done.DIR_h,done.DIR), '| acuerdo = %.1f%%' % (100*(done.DIR_h==done.DIR).mean()))
both=done[(done.DIR_h=='1')&(done.DIR=='1')]
for v in ['FUERZA','DEST','AMBITO']:
    print(f'{v} (n = {len(both)} unidades con DIR = 1 en ambas): kappa = %.3f | acuerdo = %.1f%%' % (cohen_kappa_score(both[v+'_h'],both[v]),100*(both[v+'_h']==both[v]).mean()))
nc=done[done.estrato=='nocand']
if len(nc)==0: raise SystemExit
print('No candidatas revisadas:',len(nc),'| directivas halladas por la experta:',int((nc.DIR_h=='1').sum()),'(%.1f%%)' % (100*(nc.DIR_h=='1').mean()))
