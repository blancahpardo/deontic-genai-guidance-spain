import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.edgecolor':'#8a8984','axes.linewidth':0.6})
INK='#0b0b0b'; INK2='#52514e'; SURF='#ffffff'
d=pd.read_csv('analisis/resultados/directivas.csv')
# Figura 1
order_dest=[('EST','Students'),('DOC','Teaching staff'),('COM','Whole community'),('INST','The institution')]
forces=[('PROH','Prohibition','#2a78d6','////'),('OBL','Obligation','#eb6834',''),('REC','Recommendation','#1baf7a','....'),('PERM','Permission','#eda100','xx'),('COMP','Self-commitment','#7a5cc4','\\\\')]
fig,ax=plt.subplots(figsize=(6.3,2.6),dpi=300)
for i,(code,lab) in enumerate(order_dest):
    s=d[d.DEST==code]; n=len(s); left=0
    for fc,fl,col,h in forces:
        v=100*(s.FUERZA==fc).sum()/n
        ax.barh(i,v,left=left,color=col,edgecolor=SURF,linewidth=1.5,hatch=h,height=0.62)
        if v>=6: ax.text(left+v/2,i,f'{v:.0f}%',ha='center',va='center',fontsize=7.5,color=INK,bbox=dict(boxstyle='round,pad=0.15',fc='white',ec='none',alpha=0.85))
        left+=v
    ax.text(101.5,i,f'n = {n}',va='center',fontsize=7.5,color=INK2)
ax.set_yticks(range(len(order_dest))); ax.set_yticklabels([l for _,l in order_dest],color=INK)
ax.invert_yaxis(); ax.set_xlim(0,100); ax.set_xlabel('Share of directives addressed to each group (%)',color=INK2)
for sp in ['top','right']: ax.spines[sp].set_visible(False)
ax.tick_params(colors=INK2,length=2)
handles=[plt.Rectangle((0,0),1,1,facecolor=c,hatch=h,edgecolor='white') for _,_,c,h in forces]
ax.legend(handles,[l for _,l,_,_ in forces],ncol=5,frameon=False,loc='lower center',bbox_to_anchor=(0.45,1.0),fontsize=7.5)
plt.tight_layout(); plt.savefig('manuscrito/figuras/figure1.png',dpi=300,facecolor='white',metadata={'Software':None}); plt.close()
# Figura 2
p=pd.read_csv('analisis/resultados/por_documento.csv')
p=p[(p.directivas>=10)&(p.anio.astype(str).str.match(r'^\d{4}$'))].copy(); p['anio']=p.anio.astype(int)
fig,ax=plt.subplots(figsize=(4.6,3.0),dpi=300)
rng=np.random.default_rng(7)
for k,(y,g) in enumerate(p.groupby('anio')):
    x=y+rng.uniform(-0.12,0.12,len(g))
    sz=np.clip(g.directivas,10,140)*0.9
    ax.scatter(x,g.pct_restrictiva,s=sz,color='#2a78d6',alpha=0.55,edgecolor='white',linewidth=1.2,zorder=3)
    med=g.pct_restrictiva.median()
    ax.plot([y-0.25,y+0.25],[med,med],color=INK,linewidth=2,zorder=4)
    ax.text(y+0.28,med,f'median {med:.0f}%',va='center',fontsize=7.5,color=INK)
ax.set_xticks([2023,2024,2025]); ax.set_xlim(2022.6,2025.7); ax.set_ylim(0,100)
ax.set_ylabel('Obligations + prohibitions (%)',color=INK2); ax.set_xlabel('Year of publication',color=INK2)
ax.yaxis.grid(True,color='#e6e5e0',linewidth=0.6); ax.set_axisbelow(True)
for sp in ['top','right']: ax.spines[sp].set_visible(False)
ax.tick_params(colors=INK2,length=2)
ax.text(2022.65,96,'Each dot is one document (size = number of directives)',fontsize=7,color=INK2)
plt.tight_layout(); plt.savefig('manuscrito/figuras/figure2.png',dpi=300,facecolor='white',metadata={'Software':None}); plt.close()
print(p.groupby('anio').size())
