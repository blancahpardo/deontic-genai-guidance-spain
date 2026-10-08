"""Análisis de las directivas anotadas.

Entradas: unidades_marcadas.csv, anot/lote_*.csv, ../corpus/inventario.csv
Salidas:  resultados/*.csv y resultados/resumen.txt

1. Fusiona anotaciones y unidades; elimina duplicados de maquetación.
2. Deriva la forma lingüística principal y la expresión del agente de cada directiva.
3. Calcula densidades, distribuciones y pruebas de asociación.
"""
import csv, os, re, glob, collections, math
import pandas as pd
import numpy as np
from scipy import stats
import spacy

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'resultados')
os.makedirs(OUT, exist_ok=True)
nlp = spacy.load('es_core_news_md', disable=['ner'])

units = pd.read_csv(os.path.join(BASE, 'unidades_marcadas.csv'), dtype=str).fillna('')
inv = pd.read_csv(os.path.join(BASE, '..', 'corpus', 'inventario.csv'), dtype=str).fillna('')
rows = []
for f in sorted(glob.glob(os.path.join(BASE, 'anot', 'lote_*.csv'))):
    for line in open(f, encoding='utf-8'):
        p = line.rstrip('\n').split(';')
        if len(p) >= 5:
            rows.append(dict(unidad=p[0], DIR=int(p[1]), FUERZA=p[2], DEST=p[3], AMBITO=p[4]))
ann = pd.DataFrame(rows).drop_duplicates('unidad', keep='last')  # los lotes posteriores (correcciones) prevalecen
df = units.merge(ann, on='unidad', how='left')
df['DIR'] = df['DIR'].fillna(0).astype(int)

# --- duplicados de maquetación: misma cadena normalizada (o contenida) dentro del mismo documento
def norm(s):
    return re.sub(r'\W+', ' ', s.lower()).strip()
df['norm'] = df['texto'].map(norm)
dup = set()
for doc, g in df[df.tipo == 'oracion'].groupby('doc'):
    seen = []
    for i, r in g.iterrows():
        n = r['norm']
        if len(n) < 25:
            continue
        if any(n == s or (len(n) > 60 and n in s) or (len(s) > 60 and s in n) for s in seen):
            dup.add(i)
        seen.append(n)
df['duplicado'] = df.index.isin(dup)
clean = df[~df.duplicado].copy()

# --- palabras por documento (solo oraciones, sin duplicados)
clean['palabras'] = clean['texto'].map(lambda s: len(s.split()))
words = clean[clean.tipo == 'oracion'].groupby('doc')['palabras'].sum()

d = clean[clean.DIR == 1].copy()

# --- forma lingüística principal (jerarquía: la marca más específica)
# forma asignada a mano: unidades de D13 anotadas en el barrido exhaustivo (sin marcas por palabras partidas)
FORMA_MANUAL = {'D13-0003': 'Predicado evaluativo', 'D13-0074': 'Predicado evaluativo', 'D13-0081': 'Predicado evaluativo',
    'D13-0192': 'Predicado evaluativo', 'D13-0151': 'Verbo modal',
    'D13-0080': 'Infinitivo o elemento de lista', 'D13-0082': 'Infinitivo o elemento de lista', 'D13-0088': 'Infinitivo o elemento de lista',
    'D13-0069': 'Imperativo/exhortativo', 'D13-0084': 'Imperativo/exhortativo', 'D13-0087': 'Imperativo/exhortativo',
    'D13-0098': 'Imperativo/exhortativo', 'D13-0101': 'Imperativo/exhortativo', 'D13-0147': 'Imperativo/exhortativo',
    'D13-0159': 'Imperativo/exhortativo', 'D13-0166': 'Imperativo/exhortativo'}

# forma asignada a mano: directivas del barrido exhaustivo que la regla automática deja en «Otra»
# (imperativos con mayúscula o ligaduras que spaCy no reconoce, «es preciso», listas bajo fórmula sancionadora)
FORMA_MANUAL.update({
    'D04-0015': 'Imperativo/exhortativo',
    'D04-0017': 'Imperativo/exhortativo',
    'D06-0016': 'Imperativo/exhortativo',
    'D06-0017': 'Imperativo/exhortativo',
    'D06-0034': 'Imperativo/exhortativo',
    'D06-0037': 'Imperativo/exhortativo',
    'D06-0038': 'Imperativo/exhortativo',
    'D12-0258': 'Imperativo/exhortativo',
    'D12-0290': 'Imperativo/exhortativo',
    'D12-0305': 'Imperativo/exhortativo',
    'D16-0076': 'Imperativo/exhortativo',
    'D20-0149': 'Imperativo/exhortativo',
    'D20-0233': 'Imperativo/exhortativo',
    'D20-0283': 'Imperativo/exhortativo',
    'D20-0405': 'Imperativo/exhortativo',
    'D20-0408': 'Imperativo/exhortativo',
    'D20-0414': 'Imperativo/exhortativo',
    'D22-0045': 'Imperativo/exhortativo',
    'D23-0085': 'Imperativo/exhortativo',
    'D23-0235': 'Imperativo/exhortativo',
    'D23-0236': 'Imperativo/exhortativo',
    'D23-0280': 'Imperativo/exhortativo',
    'D27-0125': 'Imperativo/exhortativo',
    'D27-0127': 'Imperativo/exhortativo',
    'D27-0190': 'Imperativo/exhortativo',
    'D30-0006': 'Imperativo/exhortativo',
    'D31-0004': 'Imperativo/exhortativo',
    'D31-0012': 'Imperativo/exhortativo',
    'D31-0016': 'Imperativo/exhortativo',
    'D01-0112': 'Predicado evaluativo',
    'D10-0028': 'Predicado evaluativo',
    'D12-0175': 'Predicado evaluativo',
    'D17-0279': 'Predicado evaluativo',
    'D17-0539': 'Predicado evaluativo',
    'D19-0076': 'Predicado evaluativo',
    'D20-0096': 'Predicado evaluativo',
    'D19-0129': 'Predicado evaluativo',
    'D19-0241': 'Predicado evaluativo',
    'D19-0447': 'Predicado evaluativo',
    'D20-0246': 'Predicado evaluativo',
    'D20-0346': 'Predicado evaluativo',
    'D21-0023': 'Predicado evaluativo',
    'D23-0009': 'Predicado evaluativo',
    'D26-0066': 'Predicado evaluativo',
    'D30-0004': 'Predicado evaluativo',
    'D03-0057': 'Infinitivo o elemento de lista',
    'D17-0718': 'Infinitivo o elemento de lista',
    'D17-0875': 'Infinitivo o elemento de lista',
    'D17-0900': 'Infinitivo o elemento de lista',
    'D22-0069': 'Infinitivo o elemento de lista',
    'D25-0194': 'Infinitivo o elemento de lista',
    'D25-0198': 'Infinitivo o elemento de lista',
    'D27-0089': 'Infinitivo o elemento de lista',
    'D28-0038': 'Infinitivo o elemento de lista',
    'D28-0040': 'Infinitivo o elemento de lista',
    'D28-0042': 'Infinitivo o elemento de lista',
    'D28-0044': 'Infinitivo o elemento de lista',
    'D28-0106': 'Infinitivo o elemento de lista',
    'D01-0106': 'Verbo realizativo',
    'D23-0230': 'Verbo realizativo',
    'D20-0199': 'Verbo modal',
})

def forma(r):
    if r['unidad'] in FORMA_MANUAL:
        return FORMA_MANUAL[r['unidad']]
    m = set(x for x in r['marcas'].split('|') if x)
    t = r['texto'].lower()
    if 'SANC' in m:
        return 'Sanción'
    if 'PART' in m:
        return 'Estatus (permitido/prohibido)'
    if r['FUERZA'] == 'COMP':
        return 'Compromiso institucional'
    if 'PERF' in m and re.search(r'\bse (recomienda|aconseja|sugiere|anima|alienta|invita|insta|exige|requiere|pide|desaconseja|permite|prohíbe|autoriza)|\b(recomendamos|aconsejamos|sugerimos|proponemos|os recordamos|te recomendamos|te invitamos)', t):
        return 'Verbo realizativo'
    if 'PRED' in m:
        return 'Predicado evaluativo'
    if 'MOD' in m:
        return 'Verbo modal'
    if 'IMP' in m or 'EVIT' in m:
        return 'Imperativo/exhortativo'
    if 'PERF' in m:
        return 'Verbo realizativo'
    if 'HEAD' in m:
        return 'Infinitivo o elemento de lista'
    if not m:
        return forma_sin_marcas(r['texto'])
    return 'Otra'

# unidades del barrido exhaustivo de no candidatas: sin marcas del filtro, la forma se deduce del texto
RE_F_MOD = re.compile(r'\b(deb(e|en|es|emos|erá|erán|ería|erían)|pued(e|en|es)|podr(á|án|ía|ían)|hay que|ha[ns]? de|tien(e|en|es) que|tenemos que|obligad[oa]s?|la obligación)\b', re.I)
RE_F_PRED = re.compile(r'\b(es|son|será|resulta|se hace|hace)\s+(muy\s+)?(necesari[oa]s?|imprescindibles?|fundamental(es)?|esencial(es)?|importantes?|clave|recomendables?|aconsejables?|convenientes?|obligatori[oa]s?)\b|\b(requisito|responsab(le|ilidad)) (ineludible|es tuya|únic)|\bes (el )?únic[oa] responsable|\bla responsabilidad (académica )?es tuya|\bes (por tanto )?responsabilidad de', re.I)
RE_F_PERF = re.compile(r'\b(se recomienda|recomendad[oa]s?|se aconseja|se sugiere|se desaconseja|apela a)\b', re.I)
def forma_sin_marcas(texto):
    t = re.sub(r'^[\W\d_]+', '', texto)
    t = re.sub(r'^[^:.;]{1,45}:\s*', '', t)          # etiqueta inicial («Recomendado:», «Datos sensibles:»)
    t = re.sub(r'^[\W\d_]+', '', t)
    t = re.sub(r'^(por ejemplo|después|además|también),?\s+', '', t, flags=re.I)
    if RE_F_PERF.search(texto):
        return 'Verbo realizativo'
    if RE_F_PRED.search(texto):
        return 'Predicado evaluativo'
    if RE_F_MOD.search(texto):
        return 'Verbo modal'
    if not t:
        return 'Otra'
    doc = nlp(t[:1].lower() + t[1:])
    toks = [x for x in doc if not x.is_punct and not x.is_space]
    if not toks:
        return 'Otra'
    v = toks[1] if toks[0].lower_ in ('no', 'nunca') and len(toks) > 1 else toks[0]
    if v.pos_ in ('VERB', 'AUX') and ('Imp' in v.morph.get('Mood') or '2' in v.morph.get('Person')
            or ('Pres' in v.morph.get('Tense') and '3' in v.morph.get('Person') and 'Sing' in v.morph.get('Number')
                and not any(c.dep_.startswith('nsubj') for c in v.children))):
        return 'Imperativo/exhortativo'
    if any('Imp' in x.morph.get('Mood') and '2' in x.morph.get('Person') for x in toks):
        return 'Imperativo/exhortativo'
    if 'Inf' in v.morph.get('VerbForm'):
        return 'Infinitivo o elemento de lista'
    if not any(x.pos_ in ('VERB', 'AUX') and 'Fin' in x.morph.get('VerbForm') for x in toks[:6]):
        return 'Infinitivo o elemento de lista'   # nominalización o elemento de lista sin verbo finito
    return 'Otra'

# --- expresión del agente
AGENT_NOUNS = r'\b(estudiante|estudiantes|estudiantado|alumnado|alumno|alumnos|alumna|profesorado|profesor|profesores|docente|docentes|pdi|investigador|investigadores|investigadoras|personal|tutor|tutora|director|directora|autor|autores|usuario|usuarios|universidad|comunidad|equipo|equipos|miembros|personas|departamentos|facultades)\b'
def agente(r):
    doc = nlp(r['texto'])
    t = r['texto'].lower()
    verbs = [x for x in doc if x.pos_ in ('VERB', 'AUX')]
    persons = collections.Counter()
    for v in verbs:
        for p in v.morph.get('Person'):
            persons[(p, tuple(v.morph.get('Number')), tuple(v.morph.get('Mood')))] += 1
    if re.search(r'\b(debes|puedes|tienes que|debéis|podéis|tienes|asegúrate|recuerda|evita|usa|utiliza|te |tu |tus |os |vuestro|vuestra|usted|su trabajo)\b', t) or any(p[0] == '2' for p in persons):
        return '2.ª persona'
    if re.search(r'\b(debemos|podemos|tenemos que|nuestr[oa]s?|nos )\b', t) or any(p[0] == '1' and 'Plur' in p[1] for p in persons):
        return '1.ª persona plural'
    if 'IMP' in r['marcas'] and not re.search(AGENT_NOUNS, t):
        return '2.ª persona'
    if re.search(AGENT_NOUNS, t) and any(c.dep_.startswith('nsubj') and re.search(AGENT_NOUNS, c.text.lower()) for c in doc):
        return 'Agente nominal explícito'
    if re.search(r'\bse (debe|deben|debería|recomienda|aconseja|sugiere|permite|prohíbe|puede|pueden|ha de|han de|exige|requiere|anima|alienta|tiene que)\b|\bhay que\b|\bes (necesario|imprescindible|importante|fundamental|esencial|recomendable|aconsejable|obligatorio|crucial|clave|conveniente)\b|\bconviene\b', t):
        return 'Impersonal / sin agente'
    if 'HEAD' in r['marcas'] or re.match(r'^[A-ZÁÉÍÓÚ][a-záéíóú]+(ar|er|ir)\b', r['texto'].strip()):
        return 'Impersonal / sin agente'
    if re.search(r'\b(debe|deben|deberá|deberán|puede|pueden|podrá|podrán)\b', t) and not re.search(AGENT_NOUNS, t):
        return 'Impersonal / sin agente'
    if re.search(AGENT_NOUNS, t):
        return 'Agente nominal explícito'
    return 'Impersonal / sin agente'

d['FORMA'] = d.apply(forma, axis=1)
d['AGENTE'] = d.apply(agente, axis=1)
d = d.merge(inv[['id', 'universidad', 'titularidad', 'anio', 'destinatarios', 'genero', 'formato']], left_on='doc', right_on='id', how='left')
d.to_csv(os.path.join(OUT, 'directivas.csv'), index=False)

# --- tablas
out = []
def w(s=''):
    out.append(str(s))

w(f'Unidades totales: {len(df)}; duplicados eliminados: {int(df.duplicado.sum())}; oraciones/elementos (sin dup.): {int((clean.tipo=="oracion").sum())}; palabras: {int(words.sum())}')
w(f'Candidatas: {int((clean.candidata=="si").sum())}; directivas: {len(d)}; densidad global: {1000*len(d)/words.sum():.2f} por 1000 palabras')

perdoc = d.groupby('doc').size().rename('directivas').to_frame().join(words.rename('palabras'), how='right').fillna(0)
perdoc['densidad'] = 1000 * perdoc.directivas / perdoc.palabras
fz = d.pivot_table(index='doc', columns='FUERZA', values='unidad', aggfunc='count', fill_value=0)
perdoc = perdoc.join(fz).fillna(0)
perdoc = perdoc.join(inv.set_index('id')[['universidad', 'titularidad', 'anio', 'destinatarios', 'genero']])
for c in ['OBL', 'PROH', 'PERM', 'REC', 'COMP']:
    if c not in perdoc:
        perdoc[c] = 0
perdoc['pct_restrictiva'] = 100 * (perdoc.OBL + perdoc.PROH) / perdoc.directivas.replace(0, np.nan)
perdoc.to_csv(os.path.join(OUT, 'por_documento.csv'))
w('\nDensidad por documento (mediana, RIC): %.2f (%.2f-%.2f)' % (perdoc.densidad.median(), perdoc.densidad.quantile(.25), perdoc.densidad.quantile(.75)))

def tabla(a, b, name):
    t = pd.crosstab(d[a], d[b])
    t.to_csv(os.path.join(OUT, f'{name}.csv'))
    pct = (100 * t.div(t.sum(axis=1), axis=0)).round(1)
    pct.to_csv(os.path.join(OUT, f'{name}_pct_fila.csv'))
    return t, pct

w('\nFUERZA global:')
fc = d.FUERZA.value_counts()
for k, v in fc.items():
    w(f'  {k}: {v} ({100*v/len(d):.1f}%)')

t, pct = tabla('DEST', 'FUERZA', 'dest_x_fuerza')
w('\nDEST x FUERZA (n):'); w(t.to_string()); w('\n% por fila:'); w(pct.to_string())

# prueba principal: estudiantado frente a profesorado
sub = d[d.DEST.isin(['EST', 'DOC']) & d.FUERZA.isin(['OBL', 'PROH', 'PERM', 'REC'])]
ct = pd.crosstab(sub.DEST, sub.FUERZA)
chi2, p, dof, exp = stats.chi2_contingency(ct)
V = math.sqrt(chi2 / (ct.values.sum() * (min(ct.shape) - 1)))
resid = (ct - exp) / np.sqrt(exp)
w(f'\nEST vs DOC x FUERZA: chi2({dof}) = {chi2:.2f}, p = {p:.3g}, V de Cramér = {V:.3f}, n = {ct.values.sum()}')
w('Residuos estandarizados:'); w(resid.round(2).to_string())
ct.to_csv(os.path.join(OUT, 'est_doc_fuerza.csv')); resid.round(2).to_csv(os.path.join(OUT, 'est_doc_residuos.csv'))

# restrictivas (OBL+PROH) frente a no restrictivas por destinatario
sub2 = sub.assign(restr=sub.FUERZA.isin(['OBL', 'PROH']))
ct2 = pd.crosstab(sub2.DEST, sub2.restr)
oddsratio, p2 = stats.fisher_exact(ct2.values)
w(f'\nRestrictivas (OBL+PROH) por destinatario:\n{ct2.to_string()}\nOR (DOC vs EST, restrictiva) = {oddsratio:.2f}, p = {p2:.3g}')

t, pct = tabla('AMBITO', 'FUERZA', 'ambito_x_fuerza')
w('\nÁMBITO x FUERZA (n):'); w(t.to_string()); w('\n% por fila:'); w(pct.to_string())
t, pct = tabla('DEST', 'AMBITO', 'dest_x_ambito')
w('\nDEST x ÁMBITO (% por fila):'); w(pct.to_string())
# ámbito dentro de las restrictivas dirigidas al estudiantado
e = d[(d.DEST == 'EST') & d.FUERZA.isin(['OBL', 'PROH'])].AMBITO.value_counts(normalize=True).mul(100).round(1)
w('\nÁmbitos de las directivas restrictivas al estudiantado (%):'); w(e.to_string())
e = d[(d.DEST == 'DOC')].AMBITO.value_counts(normalize=True).mul(100).round(1)
w('\nÁmbitos de las directivas al profesorado (%):'); w(e.to_string())

t, pct = tabla('FORMA', 'FUERZA', 'forma_x_fuerza')
w('\nFORMA x FUERZA (n):'); w(t.to_string())
w('\nFORMA global (%):'); w(d.FORMA.value_counts(normalize=True).mul(100).round(1).to_string())
t, pct = tabla('AGENTE', 'FUERZA', 'agente_x_fuerza')
w('\nAGENTE x FUERZA (n):'); w(t.to_string()); w('\n% por fila:'); w(pct.to_string())
w('\nAGENTE global (%):'); w(d.AGENTE.value_counts(normalize=True).mul(100).round(1).to_string())
t, pct = tabla('DEST', 'AGENTE', 'dest_x_agente')
w('\nDEST x AGENTE (% por fila):'); w(pct.to_string())

t, pct = tabla('genero', 'FUERZA', 'genero_x_fuerza')
w('\nGÉNERO x FUERZA (% por fila):'); w(pct.to_string()); w(t.sum(axis=1).to_string())
t, pct = tabla('titularidad', 'FUERZA', 'titularidad_x_fuerza')
w('\nTITULARIDAD x FUERZA (% por fila):'); w(pct.to_string())
ct3 = pd.crosstab(d[d.FUERZA != 'COMP'].titularidad, d[d.FUERZA != 'COMP'].FUERZA)
chi2b, pb, dofb, _ = stats.chi2_contingency(ct3)
Vb = math.sqrt(chi2b / (ct3.values.sum() * (min(ct3.shape) - 1)))
w(f'Titularidad x fuerza: chi2({dofb}) = {chi2b:.2f}, p = {pb:.3g}, V = {Vb:.3f}')
t, pct = tabla('anio', 'FUERZA', 'anio_x_fuerza')
w('\nAÑO x FUERZA (% por fila):'); w(pct.to_string()); w(t.sum(axis=1).to_string())

# tendencia a nivel de documento (documentos con al menos 10 directivas y fecha)
pdd = perdoc[(perdoc.directivas >= 10) & perdoc.anio.str.match(r'^\d{4}$')].copy()
pdd['anio_n'] = pdd.anio.astype(int)
rho, prho = stats.spearmanr(pdd.anio_n, pdd.pct_restrictiva)
w(f'\nDocumentos con >=10 directivas y fecha: {len(pdd)}; Spearman año ~ % restrictivas: rho = {rho:.2f}, p = {prho:.3g}')
w(pdd.groupby('anio_n').pct_restrictiva.describe().round(1).to_string())
rho2, prho2 = stats.spearmanr(pdd.anio_n, pdd.densidad)
w(f'Spearman año ~ densidad: rho = {rho2:.2f}, p = {prho2:.3g}')
w('\nDensidad y % restrictivas por documento:')
w(perdoc[['universidad', 'genero', 'anio', 'destinatarios', 'palabras', 'directivas', 'densidad', 'pct_restrictiva', 'OBL', 'PROH', 'PERM', 'REC', 'COMP']].round(1).to_string())

open(os.path.join(OUT, 'resumen.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
