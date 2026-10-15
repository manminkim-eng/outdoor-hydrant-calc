# 옥외소화전 v5.1.0 독립 검증 — 앱 엔진(index.html <script id="hyd-engine"> hydCalc)과 따로 짠 파이썬 구현을 무작위 대조
# usage: python3 -I verify_hyd.py <index.html> [건수]
#  · 원문: NFPC 109(제2025-28호) 제4조① · 제5조①3호 · 제6조②③ / NFTC 109(제2026-9호) 2.1.1 · 2.2.1.3 · 2.3.2 · 2.3.3
#  · KS 강관 내경 = 외경 − 2 × 두께 (KS D 3507 · KS D 3562 Sch40) — 이 파일에서 외경 · 두께로 다시 계산
#  · 압력 판정: 배관 사용압력 = ρgJ(1.2 MPa 이상이면 앱 선택지 중 KS D 3562만 적합 — NFTC 109 2.3.3.2 · NFPC 109 제6조③) · 최저 소화전 노즐압 = ρg(J − 최저 높이 − h₃)(0.7 MPa 초과 → 감압장치, 제5조①3호 단서)
#  · 참고값(호스 손실률 · 관부속 상당길이 · K · 안전율 10 % · 올림 · HP 규격)은 앱과 같은 값을 따로 옮겨 적음
import sys,json,math,random,subprocess,os,tempfile
html=open(sys.argv[1],encoding='utf-8').read(); N=int(sys.argv[2]) if len(sys.argv)>2 else 50000
a=html.index('<script id="hyd-engine">')+len('<script id="hyd-engine">'); eng=html[a:html.index('</script>',a)]
OD={'3507':{25:(34.0,3.2),32:(42.7,3.5),40:(48.6,3.5),50:(60.5,3.8),65:(76.3,4.2),80:(89.1,4.2),100:(114.3,4.5),125:(139.8,4.5),150:(165.2,5.0),200:(216.3,5.8)},
    '3562':{25:(34.0,3.4),32:(42.7,3.6),40:(48.6,3.7),50:(60.5,3.9),65:(76.3,5.2),80:(89.1,5.5),100:(114.3,6.0),125:(139.8,6.6),150:(165.2,7.1),200:(216.3,8.2)}}
INNER={'SCH10':({d:round(o-2*t,2) for d,(o,t) in OD['3507'].items()},120),'SCH40':({d:round(o-2*t,2) for d,(o,t) in OD['3562'].items()},120),
 'STS':({25:27.6,32:36.8,40:42.8,50:54.8,65:70.0,80:85.0,100:108.2,125:133.4,150:160.0,200:210.0},150),
}
FIT={40:[1.5,0.90,2.1,0.45,0.30,13.8,6.5,3.1],50:[2.1,1.20,3.0,0.60,0.39,16.5,8.4,4.0],
 65:[2.4,1.30,3.6,0.75,0.48,19.5,10.2,4.6],80:[3.0,1.80,4.5,0.90,0.60,24.0,12.0,5.7],100:[4.2,2.40,6.3,1.20,0.81,37.5,16.5,7.6],125:[5.1,3.00,7.5,1.50,0.99,42.0,21.0,10.0],
 150:[6.0,3.60,9.0,1.80,1.20,49.5,24.0,12.0],200:[6.5,3.70,14.0,4.00,1.40,70.0,33.0,15.0]}
HOSE={1:(8,None),2:(4,None)}; K={1:1.1,2:1.15}
HP=[3,5,7.5,10,15,20,25,30,40,50,60,75,100,125,150,200]
FK=['e90','e45','teeB','teeS','gate','ball','angle','check']
def py(sys_,segs):
    A=min(2,max(1,int(sys_['hydrants']))); Q=A*350; D=A*7.0             # NFPC 109 제4조① · 제5조①3호 — 2개 이상이면 2개 · 7 m³ · 350 L/min
    F=0.0
    inner,C=INNER[sys_['pipeType']]
    for s in segs:
        Di=inner.get(s['dia']); 
        if not s['flow'] or not s['dia'] or not Di: fr=0
        else: fr=10.67*(s['flow']/60000)**1.852/(C**1.852*(Di/1000)**4.87)   # m/m (SI Hazen-Williams)
        eq=FIT.get(s['dia'],FIT[100]); L=s['len']+sum(s[k]*eq[i] for i,k in enumerate(FK)); F+=fr*L
    rate,fixed=HOSE[sys_['hoseType']]; G=fixed if fixed is not None else rate*sys_['hoseLen']/100
    sub=sys_['actualHead']+F+G+25; J=math.ceil(sub*1.1)
    P=0.163*(Q/1000)*J*K[sys_['transType']]/(sys_['pumpEff']/100); hp=P*1.341
    Php=next((h for h in HP if h>=hp), math.ceil(hp/5)*5)
    rg=1000*9.80665/1e6                                                  # MPa per m (ρ = 1,000 kg/m³ · g = 9.80665 m/s²)
    Pdis=J*rg; ok=(Pdis<1.2) or sys_['pipeType']=='SCH40'                 # SCH40 = KS D 3562
    Plow=(J-sys_['lowHead']-G)*rg; hStar=(J-G)-0.7/rg
    return dict(A=A,Clpm=Q,D=D,F=F,G=G,J=J,Pkw=P,Php=Php,Pdis=Pdis,pipePressOK=ok,Plow=Plow,needPRV=Plow>0.7,hStar=hStar)
random.seed(20261015); cases=[]
for _ in range(N):
    sy=dict(hydrants=random.randint(1,10),actualHead=round(random.uniform(5,180),1),hoseLen=random.choice([15,30,45]),hoseType=random.randint(1,2),
            transType=random.randint(1,2),pumpDia=random.choice([40,50,65,80,100,125,150]),pumpEff=random.randint(10,80),
            pipeType=random.choice(['SCH10','SCH40','STS']),
            lowHead=round(random.uniform(-10,60),1))
    sg=[dict(flow=random.choice([350,700]),dia=random.choice([40,50,65,80,100,125,150,200]),len=round(random.uniform(0,120),1),
             **{k:random.randint(0,6) for k in FK}) for _ in range(random.randint(1,5))]
    cases.append((sy,sg))
tf=os.path.join(tempfile.gettempdir(),'_odh_cases.json'); json.dump(cases,open(tf,'w'))
js=os.path.join(tempfile.gettempdir(),'_odh_run.js')
open(js,'w',encoding='utf-8').write("var window=globalThis;\n"+eng+"\nconst cs=require(process.argv[2]);process.stdout.write(JSON.stringify(cs.map(([s,g])=>{const c=hydCalc(s,g);return {A:c.A,Clpm:c.Clpm,D:c.D,F:c.F,G:c.G,J:c.J,Pkw:c.Pkw,Php:c.Php,Pdis:c.Pdis,pipePressOK:c.pipePressOK,Plow:c.Plow,needPRV:c.needPRV,hStar:c.hStar}})));")
E=json.loads(subprocess.check_output(['node',js,tf]))
bad=[];keys=['A','Clpm','D','F','G','J','Pkw','Php','Pdis','pipePressOK','Plow','needPRV','hStar']
for i,((sy,sg),e) in enumerate(zip(cases,E)):
    p=py(sy,sg)
    for k in keys:
        if isinstance(p[k],bool):
            if p[k]!=e[k]: bad.append((i,k,p[k],e[k])); break
        elif abs(p[k]-e[k])>1e-9*max(1,abs(p[k])): bad.append((i,k,p[k],e[k])); break
print(f'검사 {N}건 · 불일치 {len(bad)}건'); print(bad[:5])
cnt=lambda k:sum(1 for e in E if e[k]); print(f'판정 분포 — 배관 부적합 {sum(1 for e in E if not e["pipePressOK"])}건 · 감압장치 필요 {cnt("needPRV")}건')
