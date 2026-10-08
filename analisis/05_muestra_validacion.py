"""Muestra ciega para la validación humana (acuerdo entre la anotación asistida y la experta).
- 260 unidades candidatas, estratificadas por documento (mínimo 4 por documento).
- 100 unidades no candidatas (para estimar las directivas que escapan al filtro).
Semilla fija: 2026. La hoja no muestra ninguna etiqueta del modelo."""
import pandas as pd, numpy as np, re
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font, Alignment, PatternFill
rng=np.random.default_rng(2026)
u=pd.read_csv('analisis/unidades_marcadas.csv',dtype=str).fillna('')
u=u[u.tipo=='oracion']
cand=u[u.candidata=='si']; non=u[u.candidata=='no']
N=260; per=(cand.groupby('doc').size()/len(cand)*N).round().astype(int).clip(lower=4)
sel=[]
for doc,k in per.items():
    g=cand[cand.doc==doc]; sel.append(g.sample(min(k,len(g)),random_state=int(rng.integers(1e9))))
s1=pd.concat(sel)
s2=non.sample(100,random_state=2026)
s=pd.concat([s1.assign(estrato='cand'),s2.assign(estrato='nocand')]).sample(frac=1,random_state=7).reset_index(drop=True)
s[['unidad','estrato']].to_csv('validacion/clave_muestra.csv',index=False)
wb=Workbook(); ws=wb.active; ws.title='Anotacion'
hdr=['n','unidad','encabezado (contexto)','texto','DIR (1/0)','FUERZA','DEST','AMBITO','comentario']
ws.append(hdr)
for i,r in s.iterrows(): ws.append([i+1,r.unidad,ILLEGAL_CHARACTERS_RE.sub('',r.encabezado),ILLEGAL_CHARACTERS_RE.sub('',r.texto),'','','','',''])
for c,wd in zip('ABCDEFGHI',[5,11,30,80,9,10,9,10,30]): ws.column_dimensions[c].width=wd
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
for c in ws[1]: c.font=Font(bold=True); c.fill=PatternFill('solid',fgColor='DDEBF7')
ws.freeze_panes='E2'
n=len(s)+1
for col,opts in [('E','"1,0"'),('F','"OBL,PROH,PERM,REC,COMP"'),('G','"EST,DOC,INV,COM,INST,NE"'),('H','"INTEG,TRANSP,DATOS,VERIF,DOCEN,APREND,HERRAM,ETICA,OTRO"')]:
    dv=DataValidation(type='list',formula1=opts,allow_blank=True); ws.add_data_validation(dv); dv.add(f'{col}2:{col}{n}')
ins=wb.create_sheet('Instrucciones')
for line in ['Validación de la anotación de directivas (EAIT).',
 'Anota cada fila leyendo el texto junto con su encabezado, siguiendo el libro de códigos (analisis/libro_de_codigos.md).',
 'DIR: 1 si la unidad prescribe, prohíbe, permite o aconseja una acción a un agente humano, o compromete a la institución; 0 en otro caso.',
 'Si DIR = 0, deja vacías FUERZA, DEST y AMBITO.',
 'No consultes las anotaciones del modelo (analisis/anot/) hasta terminar.',
 'Al terminar, guarda el archivo con el mismo nombre y ejecuta: python analisis/06_kappa.py']:
    ins.append([line])
ins.column_dimensions['A'].width=120
wb.save('validacion/muestra_validacion_BHP.xlsx')
print(len(s1),len(s2),len(s))
