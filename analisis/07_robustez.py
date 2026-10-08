"""Comprobaciones de robustez del contraste estudiantado/profesorado (directivas agrupadas por documento).
1) V de Cramér dejando fuera un documento cada vez.
2) Comparación intradocumento de la proporción de REC (documentos con >= 5 directivas a cada colectivo), Wilcoxon."""
import pandas as pd, math
from scipy import stats
d=pd.read_csv('analisis/resultados/directivas.csv')
x=d[d.DEST.isin(['EST','DOC'])&(d.FUERZA!='COMP')]
out=[]
for doc in sorted(x.doc.unique()):
    y=x[x.doc!=doc]; ct=pd.crosstab(y.DEST,y.FUERZA)
    c,p,df,_=stats.chi2_contingency(ct)
    out.append((doc,math.sqrt(c/(ct.values.sum()*(min(ct.shape)-1))),p))
o=pd.DataFrame(out,columns=['excluido','V','p'])
print('LOO: V min = %.3f, V max = %.3f, p max = %.2g' % (o.V.min(),o.V.max(),o.p.max()))
for g in ['EST','DOC']:
    s=x[x.DEST==g]; print(g,'n =',len(s),'| PERM+PROH = %.1f%%' % (100*s.FUERZA.isin(['PERM','PROH']).mean()))
n=x.groupby(['doc','DEST']).size().unstack()
t=x.groupby(['doc','DEST']).FUERZA.apply(lambda s:(s=='REC').mean()).unstack()[(n.EST>=5)&(n.DOC>=5)]
w=stats.wilcoxon(t.DOC,t.EST)
print('Intradocumento: %d documentos; REC mayor para DOC en %d; Wilcoxon W = %.1f, p = %.3f' % (len(t),(t.DOC>t.EST).sum(),w.statistic,w.pvalue))
o.to_csv('analisis/resultados/robustez_loo.csv',index=False)
