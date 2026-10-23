#!/usr/bin/env python3
"""MinerU architecture diagram - final clean version, all coords verified."""
S=[];A=S.append

# CSS
A('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 840">')
A('<style>text{font-family:"PingFang SC","Microsoft YaHei","SimHei","Noto Sans SC",sans-serif}')
A('.t18{font-size:18px;font-weight:700;fill:#1e293b}.t12{font-size:12px;font-weight:600;fill:#1e293b}')
A('.t11{font-size:11px;font-weight:600;fill:#334155}.t10{font-size:10px;font-weight:400;fill:#64748b}')
A('.t9{font-size:9px;font-weight:400;fill:#94a3b8}.t8{font-size:8px;font-weight:400;fill:#64748b}')
A('.t8p{font-size:8px;font-weight:600;fill:#7c3aed}.t7{font-size:7px;font-weight:400;fill:#64748b}')
A('.ct{font-size:10.5px;font-weight:700;fill:#475569;letter-spacing:.06em}')
A('.cs{font-size:9px;font-weight:400;fill:#94a3b8}</style>')

# DEFS
A('<defs>')
for k,c in [("B","#2563eb"),("P","#7c3aed"),("G","#059669"),("X","#94a3b8")]:
    A(f'<marker id="m{k}" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><polygon points="0 0,10 4,0 8" fill="{c}"/></marker>')
A('<filter id="sd" x="-2%" y="-2%" width="104%" height="108%"><feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#0f172a" flood-opacity=".05"/></filter>')
A('<linearGradient id="gr" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#2563eb" stop-opacity="0"/><stop offset="50%" stop-color="#2563eb" stop-opacity=".5"/><stop offset="100%" stop-color="#2563eb" stop-opacity="0"/></linearGradient>')
A('</defs>')

A('<rect width="1200" height="840" fill="#fff"/>')
A('<text x="600" y="32" text-anchor="middle" class="t18">MinerU 系统架构与 NER 模型结构</text>')
A('<line x1="400" y1="42" x2="800" y2="42" stroke="url(#gr)" stroke-width="1.5"/>')

# Helpers
C={"B":"#2563eb","P":"#7c3aed","G":"#059669","X":"#94a3b8"}
def B(x,y,w,h,f="#fff",s="#cbd5e1",sw="1.2",rx="6"):A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" stroke="{s}" stroke-width="{sw}"/>')
def T(x,y,tx,c="t12",a="middle"):A(f'<text x="{x}" y="{y}" text-anchor="{a}" class="{c}">{tx}</text>')
def LN(x1,y1,x2,y2,c="B",sw="1.5",d=None):
    ds=f' stroke-dasharray="{d}"' if d else ""
    A(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{C[c]}" stroke-width="{sw}"{ds} marker-end="url(#m{c})"/>')
def P(d,c="B",sw="1.5",ds=None):
    da=f' stroke-dasharray="{ds}"' if ds else ""
    A(f'<path d="{d}" fill="none" stroke="{C[c]}" stroke-width="{sw}"{da} marker-end="url(#m{c})"/>')
def CN(x,y,w,h,la,su="",ti="#f8fafc"):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{ti}" fill-opacity=".35" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="6,3" filter="url(#sd)"/>')
    A(f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="8" fill="{ti}" stroke="none"/>')
    A(f'<rect x="{x}" y="{y+14}" width="{w}" height="8" fill="{ti}" stroke="none"/>')
    A(f'<text x="{x+16}" y="{y+15}" class="ct">{la}</text>')
    if su:A(f'<text x="{x+16+len(la)*6}" y="{y+15}" class="cs">{su}</text>')
def N(cx,cy,w,h,la,su="",f="#fff",s="#cbd5e1",sw="1.2",cl="t12",cs="t10"):
    x,y=cx-w//2,cy-h//2;B(x,y,w,h,f,s,sw)
    if su:T(cx,cy-3,la,cl);T(cx,cy+12,su,cs)
    else:T(cx,cy+4,la,cl)

# ═══ 1. DOC PARSING (y:55-200) ═══
CN(30,55,1140,145,"文档解析管道","  Document Parsing Pipeline","#eff6ff")
dc=[(126,148,"PDF 文档","用户上传"),(320,148,"FastAPI","POST /upload"),
    (520,184,"mineru_runner","质量增强 · DPI=560 · OCR优化"),
    (720,148,"MinerU","do_parse()"),(920,148,"Markdown 输出","+ Layout PDF + 图片")]
for i,(cx,w,la,su) in enumerate(dc):
    N(cx,125,w,42,la,su,s="#93c5fd")
    if i<4:LN(cx+w//2,125,dc[i+1][0]-dc[i+1][1]//2-6,125,"B","1.6")

# ═══ 2. RULE ENGINE (y:220-490, h:270) ═══
CN(30,220,530,270,"规则标注引擎","  Rule-Based Annotation","#f0fdf4")
rx=295;ry=[262,322,382,442]
rd=[(180,"Markdown 文本输入",""),(200,"正则规则匹配（5类）","标准编号 · 判定结果 · 日期 · 限值 · 数字事实"),
    (160,"上下文提取",""),(180,"entities[] + snippets[]","")]
for i,(cy,(w,la,su)) in enumerate(zip(ry,rd)):
    sk="#86efac" if i<3 else "#4ade80";fl="#fff" if i<3 else "#dcfce7"
    N(rx,cy,w,42,la,su,s=sk,f=fl)
    if i<3:LN(rx,cy+21,rx,ry[i+1]-21,"B","1.5")

# ═══ 3a. NER TRAINING (y:220-590, h:370) ═══
CN(585,220,585,378,"NER 模型训练管道","  RoBERTa + CRF + FGM","#faf5ff")
mx=740

# Token row
tk_y=262;tokens=["[CLS]","零","件","是","材","料","[SEP]"]
tw,th,tg=34,20,3;tkw=len(tokens)*(tw+tg)-tg;tkx=mx-tkw//2
for j,tl in enumerate(tokens):
    tx=tkx+j*(tw+tg);B(tx,tk_y,tw,th,"#ede9fe","#c4b5fd","0.8","4");T(tx+tw//2,tk_y+14,tl,"t8")
LN(mx,tk_y+th,mx,tk_y+th+14,"P","1.2")

# Embedding
ecy=tk_y+th+14+21;N(mx,ecy,200,42,"Token Embedding","chinese-roberta-wwm-ext · 768维",s="#c4b5fd")
LN(mx,ecy+21,mx,ecy+35,"P","1.2")

# Transformer blocks (3 visible)
rw,rh,rg=210,22,8;rb=ecy+35+6
for j in range(3):
    ty=rb+j*(rh+rg);fc="#f5f3ff" if j<2 else "#ede9fe"
    B(mx-rw//2,ty,rw,rh,fc,"#c4b5fd","0.8","5")
    mid=mx-rw//2+int(rw*.55)
    A(f'<line x1="{mid}" y1="{ty+2}" x2="{mid}" y2="{ty+rh-2}" stroke="#c4b5fd" stroke-width="0.5" opacity=".4"/>')
    T(mx-rw//2+int(rw*.55//2),ty+14,"Multi-Head Attn","t8")
    T(mid+int(rw*.45//2),ty+14,"Feed Forward","t8")
    if j==0:A(f'<path d="M {mx-rw//2-6} {ty+4} L {mx-rw//2-6} {ty+rh+6}" stroke="#c4b5fd" stroke-width="0.7" fill="none" marker-end="url(#mP)"/>')

# ×12 label: gap between block2(386..408) and block3(416..438) → center 412
T(mx,rb+2*(rh+rg)-rg//2,"⋮  ×12 Transformer Blocks","t8p")

# Arrow → Linear
lbt=rb+2*(rh+rg)+rh;LN(mx,lbt,mx,lbt+14,"P","1.2")

# Linear head
lcy=lbt+14+21;N(mx,lcy,170,42,"Linear 分类头","768 → 19 (9类实体·BIO标签)",s="#a78bfa")
LN(mx,lcy+21,mx,lcy+35,"P","1.2")

# CRF Chain
cfy=lcy+35+10;T(mx,cfy-2,"CRF 线性链 (前向算法训练 / Viterbi 解码推理)","t9")
ccy=cfy+12;ctags=["B-PART","I-PART","O","B-MAT","I-MAT"];csp,cr=46,10;cx0=mx-(len(ctags)-1)*csp//2
for j,ct in enumerate(ctags):
    cx=cx0+j*csp
    A(f'<circle cx="{cx}" cy="{ccy}" r="{cr}" fill="#faf5ff" stroke="#a78bfa" stroke-width="1.2"/>')
    T(cx,ccy+4,ct,"t7" if len(ct)>4 else "t8")
    if j<len(ctags)-1:LN(cx+cr,ccy,cx0+(j+1)*csp-cr,ccy,"P","1.2")

# BIO output
ocy=ccy+cr+8+21;N(mx,ocy,170,42,"BIO 标签序列输出","",f="#ddd6fe",s="#a78bfa")
# BIO bottom=ocy+21=ccy+cr+8+42 = (cfy+12)+10+8+42 = cfy+72

# -- Training flow (right, trx=960) --
tx=960
ti=[(300,"原始标注数据","JSONL · Doccano 导出"),
    (354,"数据清洗与增强","去重·标签映射·短实体过滤"),
    (452,"CRF NLL Loss","负对数似然损失"),
    (506,"FGM 对抗训练","嵌入层扰动 ε=0.5"),
    (560,"AdamW + CosineWarmup","动态超参数 · Gradient Clip")]
for cy,la,su in ti:N(tx,cy,184,42,la,su,s="#c4b5fd",cs="t9")

# Train arrows (properly spaced: cy[i]+21 → cy[i+1]-21)
for i in range(4):LN(tx,ti[i][0]+21,tx,ti[i+1][0]-21,"P","1.3")

# Cleaning → embedding data arrow (route through gap)
# Cleaning cy=354, right items left edge=tx-92=868
# Neural net right edge=mx+100(w=200)=840, training left=868 → gap center=854
P(f"M {tx-92} {ti[1][0]} L 854 {ti[1][0]} L 854 {ecy} L 840 {ecy}","P","1.2","4,3")
A(f'<rect x="818" y="{ecy-10}" width="52" height="16" rx="3" fill="#fff" fill-opacity=".95"/>')
A(f'<text x="844" y="{ecy+2}" text-anchor="middle" class="t8">训练数据</text>')

# ═══ 3b. NER INFERENCE (y:605-790, h:185) ═══
CN(585,613,585,188,"NER 推理管道","  Inference","#fff7ed")
ix=730
ii=[(657,148,"输入文本 (Markdown)",""),
    (707,148,"分句 + Tokenize",""),
    (757,200,"RoBERTa → CRF Viterbi 解码","最优标签序列 · BIO → Entity Span")]
for cy,w,la,su in ii:N(ix,cy,w,42,la,su,s="#fdba74",cs="t9" if su=="" else "t10")
LN(ix,ii[0][0]+21,ix,ii[1][0]-21,"P","1.3")
LN(ix,ii[1][0]+21,ix,ii[2][0]-21,"P","1.3")

# 9-class sidebar
esx=1030;esy=643
B(esx-74,esy,148,130,"#fff7ed","#fdba74","1")
T(esx,esy+16,"9类实体输出","t11")
for j,et in enumerate(["零件","工艺","材料","标准编号","标准全称","尺寸公差","粗糙度","设备","工序编号"]):
    T(esx,esy+32+j*10,et,"t8")

# Inference → sidebar arrow
P(f"M {ix+100} {ii[2][0]} L {esx-74} {ii[2][0]}","P","1.2","4,3")

# ═══ INTER-CONTAINER ARROWS ═══

# Doc→Rule (blue): corridor y=208 between doc(200) and containers(220)
P(f"M 920 146 L 920 208 L {rx} 208 L {rx} 241","B","1.8")
A(f'<rect x="575" y="198" width="80" height="16" rx="3" fill="#fff" fill-opacity=".95"/>')
A(f'<text x="615" y="210" text-anchor="middle" class="t8">Markdown 文本</text>')

# Doc→Inference (blue): route left of NER containers at x=575
P("M 970 146 L 970 215 L 575 215 L 575 636 L 656 636","B","1.8")
A(f'<rect x="830" y="205" width="80" height="16" rx="3" fill="#fff" fill-opacity=".95"/>')
A(f'<text x="870" y="217" text-anchor="middle" class="t8">Markdown 文本</text>')

# Model weights: BIO→Viterbi (purple dashed), route outside right at x=1080
# BIO: right edge=mx+85=825, cy=ocy. Viterbi: cy=747, right edge=ix+100=830
P(f"M 825 {ocy} L 825 {ocy+10} L 1050 {ocy+10} L 1050 757 L 830 757","P","1.5","6,3")
A(f'<rect x="1020" y="630" width="55" height="16" rx="3" fill="#fff" fill-opacity=".95"/>')
A(f'<text x="1047" y="642" text-anchor="middle" class="t8">模型权重</text>')

# ═══ RESULTS ═══
res_y=804
B(330,res_y,540,34,"#f1f5f9","#94a3b8","1.2","7")
T(600,res_y+14,"结构化实体输出 → Web UI 结果展示","t11")
T(600,res_y+27,"9类实体：零件·工艺·材料·标准编号·标准全称·尺寸公差·粗糙度·设备·工序编号","t9")

# Rule→Results (green)
P(f"M 295 463 L 295 {res_y-5} L 380 {res_y-5}","G","1.6")
# Inference→Results (green): from Viterbi bottom=757+21=778
P(f"M 730 778 L 730 {res_y-5} L 820 {res_y-5}","G","1.6")
A(f'<rect x="510" y="{res_y-15}" width="50" height="16" rx="3" fill="#fff" fill-opacity=".95"/>')
A(f'<text x="535" y="{res_y-3}" text-anchor="middle" class="t8">实体输出</text>')

# ═══ LEGEND ═══
B(30,res_y,235,34,"#f8fafc","#e2e8f0","1","6")
T(48,res_y+14,"图例","t11","start")
LN(42,res_y+14+8,70,res_y+14+8,"B","1.6");T(78,res_y+26,"数据流","t8")
LN(125,res_y+14+8,153,res_y+14+8,"P","1.3");T(161,res_y+26,"训练/模型加载","t8")

A('</svg>')

with open("H:/Git/MinerU/论文图/mineru-architecture.svg","w",encoding="utf-8") as f:
    f.write("\n".join(S))
print(f"OK: {len(S)} lines")
