"""Comprobación ciega de la anotación exhaustiva de las no candidatas (lotes 27-52).
- Solo unidades que el filtro descartó y que se anotaron después en el barrido exhaustivo.
- Excluye las unidades de la ronda de entrenamiento y de la ronda 2.
- 150 unidades: 60 que el modelo marcó como directivas y 90 que marcó como no directivas
  (se sobrerrepresentan las directivas para poder medir también FUERZA, DEST y ÁMBITO).
- Mismo formato, mismas instrucciones. No se muestra ninguna etiqueta del modelo.
Semilla fija: 2028."""
import pandas as pd, numpy as np
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE as ILL
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
rng=np.random.default_rng(2028)
u=pd.read_csv('analisis/unidades_marcadas.csv',dtype=str).fillna('')
inv=pd.read_csv('corpus/inventario.csv',dtype=str).fillna('')
prev=set(pd.read_csv('validacion/ronda1_entrenamiento/clave_muestra.csv',dtype=str).unidad)|set(pd.read_csv('validacion/clave_muestra.csv',dtype=str).unidad)
import glob
lab={}
for f in sorted(glob.glob('analisis/anot/lote_*.csv')):
    n=f.rsplit('lote_',1)[1].split('.')[0].split('_')[0]
    if n.isdigit() and 27<=int(n)<=52:
        for line in open(f,encoding='utf-8'):
            q=line.split(';'); lab[q[0]]=q[1]
LECT={'Comunidad':'Toda la comunidad universitaria','Estudiantes':'Estudiantes','PDI':'Profesorado (PDI)'}
# contexto: frase anterior y siguiente dentro del mismo documento (solo oraciones y elementos de lista)
o=u[u.tipo=='oracion'].copy().reset_index(drop=True)
o['anterior']=o.groupby('doc').texto.shift(1).fillna('—'); o['siguiente']=o.groupby('doc').texto.shift(-1).fillna('—')
o=o[~o.unidad.isin(prev)]
nc=o[o.unidad.isin(lab.keys())].copy(); nc['m']=nc.unidad.map(lab)
s1=nc[nc.m=='1'].sample(60,random_state=int(rng.integers(1e9)))
s2=nc[nc.m=='0'].sample(90,random_state=int(rng.integers(1e9)))
s=pd.concat([s1.assign(estrato='nc_dir'),s2.assign(estrato='nc_0')]).sample(frac=1,random_state=12).reset_index(drop=True)
s=s.merge(inv[['id','universidad','titulo','destinatarios']],left_on='doc',right_on='id',how='left')
s[['unidad','estrato']].to_csv('validacion/clave_comprobacion.csv',index=False)
wb=Workbook(); ws=wb.active; ws.title='Anotacion'
hdr=['n','unidad','Universidad','Documento','El documento se dirige a','Encabezado','Frase anterior','FRASE QUE HAY QUE ANOTAR','Frase siguiente','DIR','FUERZA','DEST','AMBITO','comentario']
ws.append(hdr)
cl=lambda t: ILL.sub('',str(t))
for i,r in s.iterrows():
    ws.append([i+1,r.unidad,r.universidad,cl(r.titulo),LECT.get(r.destinatarios,r.destinatarios),cl(r.encabezado),cl(r.anterior),cl(r.texto),cl(r.siguiente),'','','','',''])
widths=[5,10,18,26,16,24,34,60,34,7,10,8,10,24]
for c,wd in zip('ABCDEFGHIJKLMN',widths): ws.column_dimensions[c].width=wd
grey=Font(color='7F7F7F',size=9)
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
    for j in (6,8): row[j].font=grey
    row[7].font=Font(bold=True,size=11)
for c in ws[1]: c.font=Font(bold=True); c.fill=PatternFill('solid',fgColor='DDEBF7'); c.alignment=Alignment(wrap_text=True,vertical='center')
for col in 'JKLM':
    for r in range(1,len(s)+2): ws[f'{col}{r}'].fill=PatternFill('solid',fgColor='FFF2CC')
ws.freeze_panes='J2'; ws.auto_filter.ref=None
n=len(s)+1
for col,opts in [('J','"1,0"'),('K','"OBL,PROH,PERM,REC,COMP"'),('L','"EST,DOC,INV,COM,INST,NE"'),('M','"INTEG,TRANSP,DATOS,VERIF,DOCEN,APREND,HERRAM,ETICA,OTRO"')]:
    dv=DataValidation(type='list',formula1=opts,allow_blank=True,showErrorMessage=True,errorTitle='Valor no válido',error='Elige un valor de la lista desplegable.')
    ws.add_data_validation(dv); dv.add(f'{col}2:{col}{n}')
ins=wb.create_sheet('Instrucciones', 0)
for line in ['LEE PRIMERO el documento «INSTRUCCIONES_anotacion.docx» (en esta misma carpeta).',
             'Anota en la hoja «Anotacion». Solo rellenas las columnas amarillas: DIR, FUERZA, DEST, AMBITO (y comentario si quieres).',
             'No ordenes ni filtres la hoja. No borres ni muevas filas o columnas.',
             'Guarda el archivo con el mismo nombre al terminar (o cada vez que hagas una pausa).']:
    ins.append([line])
ins.column_dimensions['A'].width=130
for r in ins.iter_rows():
    for c in r: c.font=Font(size=12); c.alignment=Alignment(wrap_text=True)
wb.save('validacion/comprobacion_no_candidatas_BHP.xlsx')
print(len(s1),len(s2),len(s),'solapamiento con rondas previas:',len(set(s.unidad)&prev))
