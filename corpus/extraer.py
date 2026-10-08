import sys,os,re,pdfplumber
from bs4 import BeautifulSoup
def pdf_text(p):
    out=[]
    with pdfplumber.open(p) as pdf:
        for pg in pdf.pages:
            out.append(pg.extract_text() or '')
    return '\n'.join(out), len(out)
def html_text(p):
    s=BeautifulSoup(open(p,encoding='utf-8',errors='ignore'),'html.parser')
    for t in s(['script','style','nav','header','footer','noscript','form','svg']): t.decompose()
    m=s.find('main') or s.find(id=re.compile('content|main',re.I)) or s.body or s
    return m.get_text('\n',strip=True), 0
for f in sorted(os.listdir('raw')):
    p=os.path.join('raw',f)
    try:
        kind=open(p,'rb').read(5)
        if kind.startswith(b'%PDF'):
            t,n=pdf_text(p)
        else:
            t,n=html_text(p)
    except Exception as e:
        print(f,'ERROR',e); continue
    base=os.path.splitext(f)[0]
    open(f'txt/{base}.txt','w').write(t)
    print(f'{f:32s} pages={n:3d} words={len(t.split()):6d}')
