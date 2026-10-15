# -*- coding: utf-8 -*-
"""옥외소화전 펌프 용량 계산서 사용자 매뉴얼 생성기 (MANMIN 매뉴얼 공통 엔진 사용)
   실행: MANUAL_DIR=<manual 폴더> python gen_manual_odh.py  →  <manual>/index.html
   근거(LawMCP 원문 대조 2026-10-15):
     옥외소화전설비의 화재안전성능기준(NFPC 109) 소방청고시 제2025-28호(2025. 12. 31. 일부개정, 2026. 3. 1. 시행) 제4조 · 제5조 · 제6조 · 제11조
     옥외소화전설비의 화재안전기술기준(NFTC 109) 국립소방연구원공고 제2026-9호(2026. 3. 1. 시행) 2.1 · 2.2 · 2.3
   예제 수치는 캡처 때 앱 엔진(window.HYDENG.calc)으로 계산해 기록한 _example.json 에서 가져온다.
   참고값 표(호스 손실률 · 강관 내경)는 앱 index.html 의 hyd-engine 을 node 로 읽는다."""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manual_engine import fig, T, render, B, MARKS
HERE = os.path.dirname(os.path.abspath(__file__))
EX = json.load(open(os.path.join(HERE, '_example.json'), encoding='utf-8'))
A, Bx, C = EX['A']['R'], EX['B']['R'], EX['C']['R']
IA, IB, IC = EX['A']['in'], EX['B']['in'], EX['C']['in']
APPHTML = os.path.join(B, '..', 'index.html')
JS = r"""const fs=require('fs');const s=fs.readFileSync(process.argv[1],'utf8');const a=s.indexOf('<script id="hyd-engine">')+24;
const e=s.slice(a,s.indexOf('</script>',a));var window=globalThis;eval(e);console.log(JSON.stringify({PIPE_CONFIG,HOSE_TYPES,FITTING_EQ,TRANS_TYPE,PUMP_EFF}));"""
D = json.loads(subprocess.check_output(['node', '-e', JS, APPHTML]))

VER = 'Ver-5.1'
REL = 'v5.1.0'
DATE = '2026-10-15'
PDF = '옥외소화전_사용자매뉴얼_Ver-5.1.pdf'
APP_URL = 'https://manminkim-eng.github.io/outdoor-hydrant-calc/'
APP = '옥외소화전 펌프 용량 계산서'
NFPC = '옥외소화전설비의 화재안전성능기준(NFPC 109) 소방청고시 제2025-28호(2026. 3. 1. 시행)'
NFTC = '옥외소화전설비의 화재안전기술기준(NFTC 109) 국립소방연구원공고 제2026-9호(2026. 3. 1. 시행)'
LAW = f'{NFPC}, {NFTC}'

# ── 예제 검산(앱 엔진 결과 ↔ 매뉴얼 서술) ──
assert A['A'] == 2 and A['Clpm'] == 700 and abs(A['D'] - 14) < 1e-9 and A['J'] == 43 and A['Php'] == 15 and not A['needPRV'] and A['pipePressOK'], A
assert Bx['A'] == 2 and Bx['J'] == 54 and Bx['Php'] == 15 and abs(Bx['G'] - 3.6) < 1e-9, Bx
assert C['J'] == 96 and C['Php'] == 30 and C['needPRV'] and C['pipePressOK'] and abs(C['hStar'] - 23.42) < 0.01, C
f1 = lambda v: f'{v:,.1f}'
f2 = lambda v: f'{v:,.2f}'
f3 = lambda v: f'{v:,.3f}'

def F(sid, cap, legend=None, **kw):
    if legend is None:
        legend = [k['label'] for k in MARKS.get(sid, {}).get('marks', [])] or None
    return fig(sid, cap, legend, **kw)

FLOW_SVG = r"""<svg viewBox="0 0 900 210" role="img" aria-label="옥외소화전 펌프 산정 흐름: 설치개수로 토출량과 수원을 정하고, 실양정과 배관 호스 마찰손실에 노즐 25 m를 더해 전양정을 구한 뒤 전동기 동력과 압력 판정을 거쳐 A4 계산서로 남긴다">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2D3A8C"/></marker></defs>
<style>.b{fill:#E9ECF8;stroke:#2D3A8C;stroke-width:1.5}.o{fill:#FDF1E7;stroke:#C97A3A;stroke-width:1.5}.t{font:600 14px 'Noto Sans KR','Noto Sans KR Local',sans-serif;fill:#1A1A2E}.s{font:12px 'Noto Sans KR','Noto Sans KR Local',sans-serif;fill:#4A4F66}.l{stroke:#2D3A8C;stroke-width:1.6;fill:none;marker-end:url(#ar)}</style>
<rect class="b" x="10" y="20" width="200" height="72" rx="10"/><text class="t" x="22" y="48">① 수원 · 토출량</text><text class="s" x="22" y="72">2개 한도 × 7 m³ · 350 L/min</text>
<rect class="b" x="240" y="20" width="200" height="72" rx="10"/><text class="t" x="252" y="48">② 전양정</text><text class="s" x="252" y="72">h₁ + h₂ + h₃ + 25 m</text>
<rect class="b" x="470" y="20" width="200" height="72" rx="10"/><text class="t" x="482" y="48">③ 전동기 동력</text><text class="s" x="482" y="72">0.163 Q H K ÷ η → HP</text>
<rect class="o" x="700" y="20" width="190" height="72" rx="10"/><text class="t" x="712" y="48">④ A4 계산서</text><text class="s" x="712" y="72">인쇄 · PDF · JPG</text>
<path class="l" d="M210,56 L238,56"/><path class="l" d="M440,56 L468,56"/><path class="l" d="M670,56 L698,56"/>
<rect class="b" x="240" y="122" width="430" height="66" rx="10"/><text class="t" x="252" y="148">압력 판정 — 1.2 MPa 배관 · 0.7 MPa 감압장치</text><text class="s" x="252" y="171">NFTC 109 2.3.3 · NFPC 109 제5조①3호 단서</text>
<path class="l" d="M340,92 L340,120"/>
</svg>"""

EXTRA_CSS = """<style>
#fig-s12_formula,#fig-s13_formula_src,#fig-s14_formula_head{max-width:560px}
#fig-s16_a4page{max-width:560px}
.k1 td:first-child,.k1 th:first-child{white-space:nowrap}
@media (max-width:1240px){.eq{white-space:pre-wrap;word-break:keep-all}}
.eq .c{display:block;margin-top:2px}
.pair>div{min-width:0}
.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;align-items:start}
@media (max-width:760px){.tri{grid-template-columns:1fr}}
@media print{
  figure.shot{max-width:none!important}
  figure.shot .frame{width:fit-content;max-width:100%}
  figure.shot img{width:auto;height:auto;max-width:100%;max-height:118mm}
  #fig-s16_a4page img{max-height:200mm}
  figure.narrow img{max-height:105mm}
  .pair{grid-template-columns:1fr 1fr}.tri{grid-template-columns:repeat(3,1fr)}
  .brk .tbl{break-inside:auto}.brk tr{break-inside:avoid}.brk thead{display:table-header-group}
}
</style>"""
K = lambda t: '<div class="k1">' + t + '</div>'
BR = lambda t: '<div class="brk">' + t + '</div>'

TOC = [
 ('ch0', '0. 이 매뉴얼에 대하여', []),
 ('ch1', '1. 한눈에 보기', [('s1-1', '화면 구성'), ('s1-2', '작업 탭·근거 표시'), ('s1-3', '설치·보관·매뉴얼')]),
 ('ch2', '2. 1분 따라하기', []),
 ('ch3', '3. 화면별 기능 상세', [('s3-1', '프로젝트 정보'), ('s3-2', '시스템 파라미터'), ('s3-3', '배관 구간 입력'), ('s3-4', '수원 용량'), ('s3-5', '펌프 양정 · 압력 판정'), ('s3-6', '전동기 동력'), ('s3-7', '사례 — 물류창고'), ('s3-8', '사례 — 경사지 감압'), ('s3-9', '계산식 안내 창'), ('s3-10', 'A4 계산서·출력'), ('s3-11', '휴대전화 화면')]),
 ('ch4', '4. 법령 해설', [('s4-1', '근거 체계'), ('s4-2', '수원'), ('s4-3', '가압송수장치'), ('s4-4', '설치 · 호스 · 배관'), ('s4-5', '마찰손실·강관 내경'), ('s4-6', 'MANMIN 참고값'), ('s4-7', 'v5.1.0 정정')]),
 ('ch5', '5. 실무 작업 방법', [('s5-1', '단계별 절차'), ('s5-2', '설계 · 승인 전 확인')]),
 ('ch6', '6. 문제 해결·FAQ', []),
 ('ch7', '부록', [('a1', '예제 입력값'), ('a2', '예제 결과'), ('a3', '버전 변경 내역'), ('a4', '용어')]),
]
S = []
S.append(f"""{EXTRA_CSS}<section class="ch" id="ch0"><h2><span class="n">00</span>이 매뉴얼에 대하여</h2>
<p class="lead">{APP}는 옥외소화전설비의 <b>수원</b>, <b>펌프 토출량 · 전양정</b>, <b>전동기 동력</b>과 <b>압력 판정(배관 사용압력 · 감압장치)</b>을 한 화면에서 산정해 A4 계산서로 정리하는 도구입니다. 근거는 {LAW}입니다.</p>
{K(T([
 ['대상 프로그램', f'{APP} <b>MANMIN {VER}</b>({REL}) — 탭 막대 「📘 매뉴얼」 버튼으로 이 문서가 열립니다'],
 ['접속 주소', f'<a href="{APP_URL}" target="_blank" rel="noopener">manminkim-eng.github.io/outdoor-hydrant-calc</a>'],
 ['매뉴얼 판', f'<b>{VER}</b> (화면 표기와 같은 판 번호, 초판) · {DATE} · 작성 김만민 건축사(㈜대성건축사사무소)'],
 ['내려받기', f'<a href="{PDF}" download>PDF(A4)</a> · <a href="../index.html">{APP} 열기</a>'],
 ['예제', f'본문 그림은 예제 A(익산 공장 — 옥외소화전 3개 · 실양정 8 m)로 캡처했습니다 — <b>토출량 {A["Clpm"]} L/min · 수원 {f3(A["D"])} m³ · 전양정 {A["J"]} m · {A["Php"]:g} HP</b>. 예제 B(물류창고 긴 단지 배관) · C(경사지 — 감압장치)는 <a href="#a2">부록 A2</a>'],
 ['근거 법령', f'{LAW} — LawMCP(국가법령정보센터) 원문 대조({DATE})'],
 ['읽는 순서', '처음이면 1장 → 2장(따라하기) → 필요할 때 3장(화면별 상세). 설계도서 · 소방시설 착공신고에 쓰기 전에는 4장(법령 해설) · 5장(작업 방법)'],
], ['항목', '내용']))}
<div class="note"><b>표기</b>그림 위 주황색 번호(①②…)는 그림 아래 범례 번호와 같습니다. 그림을 누르면 크게 볼 수 있습니다. 「제4조」 · 「제5조」는 NFPC 109의 조문, 「2.1.1」처럼 점으로 이은 번호는 NFTC 109의 절입니다. 유량 단위는 L/min(화면 표기 ℓ/min), 수두 단위는 m입니다.</div>
<div class="warn"><b>책임 한계</b>산정값은 입력값에 따른 예비 · 검토용 결과입니다. 펌프 양정 안전율 10 % · 올림, 65 mm 호스 손실률, 관부속 상당길이, 전달계수 · 효율, Hazen-Williams C값은 화재안전기준에 수치가 없는 <b>MANMIN 참고값</b>입니다(<a href="#s4-6">4-6</a>). 압력 판정의 최저 소화전 방수압은 배관 마찰을 빼지 않은 추정값입니다. 실제 펌프 선정은 제조사 성능곡선과 소방시설 설계 기준에 따라 소방기술사 · 설계자가 확인하십시오.</div>
</section>""")

S.append(f"""<section class="ch" id="ch1"><h2><span class="n">01</span>한눈에 보기</h2>
<p class="lead">설치 없이 브라우저에서 바로 실행되는 단일 페이지 앱(PWA)입니다. 입력한 내용은 브라우저 안에서만 계산되며 서버로 전송되지 않습니다.</p>
<div class="cards">
<div class="card"><h5>무엇을 산정하나</h5><p>동시사용 개수 · 펌프 토출량 · 수원 · 전양정 · 전동기 동력(kW · HP)</p></div>
<div class="card"><h5>압력 판정</h5><p>토출압력 1.2 MPa 이상이면 배관 재질(KS D 3562 등), 최저 소화전 방수압 0.7 MPa 초과면 감압장치</p></div>
<div class="card"><h5>배관 마찰손실</h5><p>구간마다 유량 · 관경 · 길이 · 관부속을 넣으면 Hazen-Williams 식으로 손실 · 유속을 계산</p></div>
</div>
<h3 id="s1-1">1-1. 화면 구성</h3>
{F('s01_overview', '전체 화면 — ① 데이터 입력 탭(예제 A)')}
{K(T([
 ['헤더 · 탭', '「① 데이터 입력」 → 「② 계산 결과」 → 「③ 계산서 출력」, 오른쪽 끝 「📘 매뉴얼」'],
 ['요약 바', '어느 탭에 있든 토출량 · 수원 · 전양정 · 전동기 · 배관 · 호스 마찰을 한 줄로 보여 줍니다'],
 ['Ⅰ-0 · Ⅰ-1 · Ⅰ-2', '프로젝트 정보 → 시스템 파라미터 → 배관 구간 — 값을 바꾸면 즉시 다시 계산됩니다'],
 ['계산식 안내', '오른쪽 「📐 계산식 안내」 — 이용방법 · 수원 · 토출량 · 전양정 · 동력 · 관부속 5개 탭 창'],
], ['영역', '내용']))}
<h3 id="s1-2">1-2. 작업 탭·근거 표시</h3>
{F('s02_header', '헤더 — 작업 탭과 근거 표시')}
<p>헤더 오른쪽에는 적용 기준 NFTC 109와 <b>[공고 제2026-9호 · 시행 2026. 3. 1.]</b>이 표시됩니다.</p>
<h3 id="s1-3">1-3. 설치·보관·매뉴얼</h3>
{K(T([
 ['설치', '브라우저 「홈 화면에 추가」 또는 설치 안내 — 설치하면 오프라인에서도 열립니다(앱 본체만 — 매뉴얼은 온라인 전용)'],
 ['보관', '계산 결과는 A4 계산서(인쇄 · PDF · JPG)로 남깁니다. 앱은 입력값을 서버에 저장하지 않습니다'],
 ['매뉴얼', '탭 막대 오른쪽 「📘 매뉴얼」 — 이 문서(HTML)와 PDF(A4)'],
], ['항목', '내용']))}
</section>""")

S.append(f"""<section class="ch" id="ch2"><h2><span class="n">02</span>1분 따라하기</h2>
<p class="lead">예제 A — 익산 공장, 옥외소화전 3개입니다. 아래 순서대로 넣으면 <b>토출량 {A['Clpm']} L/min · 전양정 {A['J']} m · 전동기 {A['Php']:g} HP</b>가 나옵니다.</p>
<ol class="steps">
<li><b class="t">① 프로젝트 정보</b>공사명 「익산시 ○○동 공장 신축공사」, 설계자, 작성일 — A4 계산서 표제에 들어갑니다(<a href="#s3-1">3-1</a>).</li>
<li><b class="t">② 시스템 파라미터</b>소화전 3개 · 실양정 8 m · 최저 호스접결구 펌프 기준 6 m · 65 mm 고무내장호스 30 m(2본) · 100A · 효율 60 % · 전동기 직결 · KS D 3507(<a href="#s3-2">3-2</a>).</li>
<li><b class="t">③ 배관 구간</b>펌프 토출 100A 700 L/min 30 m · 옥외 매설 80A 350 L/min 60 m · 소화전 분기 65A 350 L/min 5 m와 관부속 수량 → 마찰손실 합계 <b>{f3(A['F'])} m</b>(<a href="#s3-3">3-3</a>).</li>
<li><b class="t">④ 결과 — 전양정</b>「② 계산 결과」 → (8 + {f3(A['F'])} + {f3(A['G'])} + 25) × 1.1 = {f3(A['Jraw'])} → 올림 <b>{A['J']} m</b> · 토출압력 {f3(A['Pdis'])} MPa · 최저 소화전 {f3(A['Plow'])} MPa(<a href="#s3-5">3-5</a>).</li>
<li><b class="t">⑤ 수원 · 동력</b>2개 × 350 L/min = {A['Clpm']} L/min · 수원 2 × 7 = <b>{f3(A['D'])} m³</b> · 0.163 × 0.700 × {A['J']} × 1.1 ÷ 0.6 = {f3(A['Pkw'])} kW → <b>{A['Php']:g} HP</b>(<a href="#s3-4">3-4</a> · <a href="#s3-6">3-6</a>).</li>
<li><b class="t">⑥ A4 계산서</b>「③ 계산서 출력」에서 「🖨️ 인쇄 · PDF」 또는 「🖼️ JPG 저장」(<a href="#s3-10">3-10</a>).</li>
</ol>
{K(T([
 ['소화전 기준개수', '3개 설치 → 2개 적용(NFPC 109 제4조① · NFTC 109 2.1.1)'],
 ['펌프 토출량', f'2 × 350 = <b>{A["Clpm"]} L/min</b>(제5조①3호 · 350 L/min 이상의 계산값)'],
 ['수원', f'2 × 7 m³ = <b>{f3(A["D"])} m³</b>(350 L/min × 20분)'],
 ['배관 · 호스 마찰손실', f'{f3(A["F"])} m · {f3(A["G"])} m(4 m/100 m × 30 m)'],
 ['전양정', f'{f3(A["Jraw"])} → <b>{A["J"]} m</b>(안전율 10 % · 올림 — MANMIN 참고값)'],
 ['전동기', f'{f3(A["Pkw"])} kW = {f3(A["Pkw"]*1.341)} HP → <b>{A["Php"]:g} HP</b>'],
 ['압력 판정', f'토출압력 {f3(A["Pdis"])} MPa(1.2 MPa 미만 — KS D 3507 가능) · 최저 소화전 {f3(A["Plow"])} MPa(감압장치 불요, 추정)'],
], ['항목', '예제 A']))}
<div class="tip"><b>확인</b>노즐선단 방수압력 0.25 MPa(25 m)는 「이상」 기준이고, 하나의 옥외소화전 방수압이 0.7 MPa를 넘으면 호스접결구 인입측에 감압장치를 둡니다(NFPC 109 제5조①3호 단서). 경사지처럼 소화전 높이 차가 크면 <a href="#s3-8">3-8</a>을 보십시오.</div>
</section>""")

S.append(f"""<section class="ch" id="ch3"><h2><span class="n">03</span>화면별 기능 상세</h2>
<h3 id="s3-1">3-1. 프로젝트 정보</h3>
{F('s03_project', 'Ⅰ-0. 프로젝트 정보')}
<p>공사명 · 설계자 · 작성일은 A4 계산서 머리에 그대로 들어갑니다.</p>
<h3 id="s3-2">3-2. 시스템 파라미터</h3>
{F('s04_params', 'Ⅰ-1. 옥외소화전 시스템 파라미터 — 예제 A')}
{K(T([
 ['A. 동시사용 소화전 수', '옥외소화전 설치개수 — 2개 이상이면 2개로 계산합니다(제4조①)'],
 ['F. 실양정', '펌프(수원 수면)에서 가장 높은 · 먼 옥외소화전 호스접결구까지의 높이(흡입 + 토출)'],
 ['F-1. 최저 소화전 호스접결구 높이', '펌프 기준 높이(펌프보다 낮으면 음수) — 감압장치 판정에만 쓰고 계산값은 바뀌지 않음(<a href="#s3-5">3-5</a>)'],
 ['G. 호스 길이 · 종류', '15 · 30 · 45 m(1본 15 m) · 65 mm 아마 · 고무내장(제6조②) — 수평거리 40 m 이하 배치(제6조①1호)'],
 ['펌프 구경 · 효율 · 전달방식', '효율은 직접 입력(입력란 아래 구경별 참고값) · 전동기 직결 K 1.1 / 그 밖의 원동기 1.15'],
 ['배관 종류', 'KS D 3507(백관) · KS D 3562 Sch40(흑관) · STS(KS D 3576 · 3595) — 내경과 C값이 바뀝니다(<a href="#s4-5">4-5</a>). 토출압력 1.2 MPa 이상인데 KS D 3562 외를 고르면 ⚠'],
], ['항목', '설명']))}
<h3 id="s3-3">3-3. 배관 구간 입력</h3>
{F('s05_segments', 'Ⅰ-2. 배관 구간 데이터 — 예제 A')}
<p>구간마다 유량 · 관경 · 직관 길이와 관부속(90° · 45° 엘보, 분류 · 직류 티, 게이트 · 볼 · 앵글 · 체크 밸브) 수량을 넣으면, 상당직관 = 직관 + Σ(수량 × 상당길이), 손실수두 = 마찰계수(m/100 m) × 상당직관 ÷ 100이 줄마다 계산되고 합계가 h₂가 됩니다. 유속이 4 m/s를 넘으면 ⚠ 표시가 나는데, 옥외소화전 기준에는 유속 규정이 없어 옥내소화전 NFTC 102 2.3.5를 <b>참고로 준용</b>한 것입니다. 예제 A의 구간별 유속은 {', '.join(f2(v) for v in A['vel'])} m/s입니다.</p>
<h3 id="s3-4">3-4. 수원 용량</h3>
{F('s06_source', 'Ⅱ-1. 수원 용량 산정 — 예제 A')}
<p>A = min(설치개수, 2), C = A × 350 L/min, D = A × 7 m³(= 350 L/min × 20분)입니다. 예제 A: 2개 · {A['Clpm']} L/min · <b>{f3(A['D'])} m³</b>. 옥외소화전은 옥상수조 규정이 없습니다.</p>
<h3 id="s3-5">3-5. 펌프 양정 · 압력 판정</h3>
{F('s07_head', 'Ⅱ-2. 펌프 양정 계산 — 예제 A')}
<p>전양정 J = (h₁ 실양정 + h₂ 배관 마찰 + h₃ 호스 마찰 + h₄ 노즐 25 m) × 1.1 → 올림입니다. 안전율 10 %와 올림은 MANMIN 참고값입니다 — 화재안전기준에는 펌프 양정 식이 없고, 고가수조 낙차(NFTC 109 식 2.2.2.1 H = h₁ + h₂ + 25)와 압력수조 압력(식 2.2.3.1)만 같은 구성으로 정해져 있습니다.</p>
{K(T([
 ['S. 토출압력 환산', f'J × 0.0098 = {f3(A["Pdis"])} MPa — 배관 사용압력이 1.2 MPa 이상이면 KS D 3562 · 3583(NFTC 109 2.3.3.2) · NFPC 109 제6조③은 KS D 5301도 허용 — 앱 선택지 중에는 KS D 3562만 「배관 적합」'],
 ['T. 최저 소화전 노즐 방수압(추정)', f'(J − 최저 소화전 높이 − h₃) × 0.0098 = ({A["J"]} − 6 − {f3(A["G"])}) × 0.0098 = {f3(A["Plow"])} MPa → 0.7 MPa 이하. 넘으면 「감압장치 필요」와 감압 검토 높이(제5조①3호 단서 · NFTC 109 2.2.1.3)'],
 ['추정의 한계', '배관 마찰손실을 빼지 않아 실제보다 크게(안전 쪽) 나오며, 소화전 하나만 쓸 때 펌프 양정이 오르는 성능곡선 효과는 넣지 않았습니다 — 감압 범위는 제조사 곡선으로 확인'],
], ['항목', '내용']))}
<h3 id="s3-6">3-6. 전동기 동력</h3>
{F('s08_power', 'Ⅱ-3. 전동기 동력 계산 — 예제 A')}
<p>P = 0.163 × Q(m³/min) × H(m) × K ÷ η [kW] — 0.163은 ρg ÷ 60,000(물 1,000 kg/m³ · 9.8 m/s²)입니다. 이론값을 HP(× 1.341)로 바꿔 3 · 5 · 7.5 · 10 · 15 · 20 … HP 표준 규격 중 바로 위 값을 고릅니다. 예제 A: {f3(A['Pkw'])} kW = {f2(A['Pkw']*1.341)} HP → <b>{A['Php']:g} HP</b>.</p>
<h3 id="s3-7">3-7. 사례 — 물류창고</h3>
<div class="pair"><div>{F('s09_b_head', '예제 B — 전양정(긴 단지 배관 · 아마호스 45 m)')}</div><div>{F('s10_b_power', '예제 B — 전동기 동력')}</div></div>
<p>옥외소화전이 6개여도 계산은 <b>2개</b>입니다(제4조①). 단지를 도는 배관이 길어 h₂ = {f3(Bx['F'])} m, 65 mm 아마호스 45 m(3본)의 h₃ = {f3(Bx['G'])} m가 커져 전양정 <b>{Bx['J']} m</b> · {f3(Bx['Pkw'])} kW → <b>{Bx['Php']:g} HP</b>입니다. 750배 이상의 특수가연물을 저장 · 취급하는 공장 · 창고는 옥외소화전 5 m 이내에 방수총을 따로 둡니다(제6조①3호) — 방수총 수량은 이 앱이 계산하지 않습니다.</p>
<h3 id="s3-8">3-8. 사례 — 경사지 감압</h3>
{F('s11_c_head', '예제 C — 경사지 연수원(최저 소화전이 펌프보다 5 m 아래)')}
<p>가장 높은 소화전까지 실양정 55 m라 전양정이 <b>{C['J']} m</b>({f3(C['Pkw'])} kW → {C['Php']:g} HP)입니다. 토출압력 {f3(C['Pdis'])} MPa로 1.2 MPa 미만이라 백관도 쓸 수 있지만, 펌프보다 5 m 낮은 소화전의 방수압이 <b>{f3(C['Plow'])} MPa</b>로 0.7 MPa를 넘어 <b>펌프 기준 {f1(C['hStar'])} m 미만 호스접결구에 감압장치</b>를 검토합니다(제5조①3호 단서).</p>
<h3 id="s3-9">3-9. 계산식 안내 창</h3>
<div class="tri"><div>{F('s12_formula', '이용방법')}</div><div>{F('s13_formula_src', '수원 · 토출량')}</div><div>{F('s14_formula_head', '전양정 산출')}</div></div>
<p>오른쪽 「📐 계산식 안내」는 이용방법 · 수원 · 토출량 · 전양정 산출 · 동력 계산 · 관부속 참고 5개 탭입니다. 식마다 근거 조문과 MANMIN 참고값 여부를 적어 두었습니다.</p>
<h3 id="s3-10">3-10. A4 계산서·출력</h3>
{F('s15_a4', '③ 계산서 출력 탭')}
{F('s16_a4page', 'A4 옥외소화전 펌프 용량 계산서 — 예제 A')}
<p>계산서는 Ⅱ-1 수원(A ~ D) · Ⅱ-2 양정(E ~ J)과 압력 판정(S · T) · Ⅱ-3 동력(K ~ Q) · 배관 마찰손실 상세표 · Ⅱ-4 펌프 선정 결과 · 적용 법령 및 기준 순이며, 화면과 인쇄 · JPG가 같은 내용입니다.</p>
<h3 id="s3-11">3-11. 휴대전화 화면</h3>
<div class="tri"><div>{fig('s17_mobile_main', '데이터 입력', narrow=True)}</div><div>{fig('s18_mobile_result', '계산 결과', narrow=True)}</div><div>{fig('s19_mobile_a4', '계산서 출력', narrow=True)}</div></div>
<p>좁은 화면에서는 입력 칸이 한 줄로 쌓이고, 탭 막대는 좌우로 밀어서 봅니다(「📘 매뉴얼」은 오른쪽 끝). A4 계산서는 화면 폭에 맞춰 축소해 보여 주며 인쇄 · JPG는 원본 A4 크기로 나옵니다.</p>
</section>""")

P = D['PIPE_CONFIG']
pipe_rows = [[f'{d}A', f"{P['SCH10']['inner'][str(d)]:.1f}", f"{P['SCH40']['inner'][str(d)]:.1f}", f"{P['STS']['inner'][str(d)]:.1f}"] for d in [40, 50, 65, 80, 100, 125, 150, 200]]
H = D['HOSE_TYPES']
S.append(f"""<section class="ch" id="ch4"><h2><span class="n">04</span>법령 해설</h2>
<h3 id="s4-1">4-1. 근거 체계</h3>
{BR(K(T([
 ['소방시설법 시행령 별표 4 제1호사목', '옥외소화전설비를 설치해야 하는 특정소방대상물(NFPC 109 제2조)'],
 ['NFPC 109 (성능기준 · 고시)', '제4조 수원 · 제5조 가압송수장치 · 제6조 배관 등 · 제11조 겸용 — 소방청고시 제2025-28호(2025. 12. 31. 일부개정, 2026. 3. 1. 시행)'],
 ['NFTC 109 (기술기준 · 공고)', '2.1 수원 · 2.2 가압송수장치 · 2.3 배관 등 — 국립소방연구원공고 제2026-9호(2026. 3. 1. 시행)'],
 ['경과조치', 'NFPC 109 부칙(제2022-43호) 제2조 — 시행 전 건축허가 등을 신청 · 신고했거나 착공신고한 대상은 종전 기준, 개정 기준이 유리하면 그에 따를 수 있음'],
], ['기준', '내용'])))}
<p class="mono" style="font-size:13px;color:var(--text2)">LawMCP(국가법령정보센터 행정규칙) 원문 대조 {DATE}</p>
<h3 id="s4-2">4-2. 수원</h3>
<div class="eq">수원 = 옥외소화전 설치개수(2개 이상이면 2개) × 7 m³ 이상<span class="c">NFPC 109 제4조① · NFTC 109 2.1.1 — 7 m³ = 350 L/min × 20분</span></div>
{K(T([
 ['1개 설치', '1 × 7 = 7 m³ · 토출량 350 L/min'],
 ['2개 이상 설치', '2 × 7 = 14 m³ · 토출량 700 L/min'],
 ['전용 · 유효수량', '수조로 두면 소방소화설비 전용(제4조②) · 겸용 수조는 풋밸브 · 흡수구 사이의 수량만 유효수량(제4조③) · 다른 설비와 겸용하면 저수량 · 토출량은 각 설비 합계(제11조① · ②)'],
], ['구분', '기준']))}
<h3 id="s4-3">4-3. 가압송수장치</h3>
{K(T([
 ['방수압 · 방수량', '옥외소화전(2개 이상이면 2개)을 동시에 사용할 때 노즐선단 <b>0.25 MPa 이상 · 350 L/min 이상</b>(제5조①3호 · NFTC 109 2.2.1.3)'],
 ['감압장치', '하나의 옥외소화전을 사용하는 노즐선단 방수압이 0.7 MPa를 넘으면 호스접결구 인입측에 감압장치(제5조①3호 단서) — 앱 T 항목'],
 ['펌프', '전용(제5조①4호) · 체절운전 시 정격토출압력 140 % 이하, 150 % 유량에서 65 % 이상 · 성능시험배관(제5조①6호)'],
 ['고가 · 압력수조', '낙차 H = h₁ + h₂ + 25 m(NFTC 109 식 2.2.2.1) · 압력 P = p₁ + p₂ + p₃ + 0.25 MPa(식 2.2.3.1) — 20분 이상 유지(제5조② · ③)'],
], ['항목', '기준']))}
<h3 id="s4-4">4-4. 설치 · 호스 · 배관</h3>
{K(T([
 ['배치', '특정소방대상물 각 부분에서 하나의 옥외소화전까지 수평거리 40 m 이하(제6조①1호) · 호스접결구 높이 지면에서 0.5 ~ 1 m(제6조①2호 · NFTC 109 2.3.1.2)'],
 ['방수총', '750배 이상 특수가연물 저장 · 취급 공장 · 창고는 옥외소화전 5 m 이내 방수총(제6조①3호, 2025. 12. 31. 개정)'],
 ['호스', '구경 65 mm(제6조② · NFTC 109 2.3.2) · 소화전함은 옥외소화전마다 5 m 이내(제7조①)'],
 ['배관 재질 · 사용압력', '1.2 MPa 미만: KS D 3507 · KS D 5301(습식) · KS D 3576 · 3595 · KS D 4311(NFTC 109 2.3.3.1) / 1.2 MPa 이상: KS D 3562 · 3583(2.3.3.2) — NFPC 109 제6조③은 KS D 3562 · KS D 5301 · 동등 이상을 듦 — 앱 S 항목'],
 ['유속', '옥외소화전 기준에는 유속 규정이 없음 — 앱의 4 m/s 경고는 NFTC 102 2.3.5 준용 참고'],
], ['항목', '기준']))}
<h3 id="s4-5">4-5. 마찰손실·강관 내경</h3>
<div class="eq">h = 10.67 × L × Q¹·⁸⁵² ÷ (C¹·⁸⁵² × D⁴·⁸⁷)   [m] — Q(m³/s) · D(m) · L 상당직관(m)<span class="c">Hazen-Williams 식(SI) — 화면은 100 m당 손실(m/100 m)로 표시</span></div>
{BR(T(pipe_rows, ['호칭', 'KS D 3507 (백관)', 'KS D 3562 Sch40 (흑관)', 'STS (참고)'], num_cols=(1, 2, 3)))}
<p>강관 내경(mm)은 KS 외경 − 2 × 두께로 계산한 값입니다(v5.1.0 — 이전 판은 일부 ASME · 다른 규격 값이었음). STS 내경은 제품마다 달라 MANMIN 참고값입니다. C값은 강관 120 · STS 150(MANMIN 참고값)입니다.</p>
<h3 id="s4-6">4-6. MANMIN 참고값</h3>
{K(T([
 ['펌프 전양정 안전율 · 올림', '(h₁ + h₂ + h₃ + 25) × 1.1 → 올림 — 화재안전기준에 펌프 양정 식 · 안전율 수치 없음'],
 ['65 mm 호스 마찰손실', ' · '.join(f"{H[k]['label']} {H[k]['rate']} m / 100 m" for k in sorted(H, key=int)) + ' — 실무 교재 값'],
 ['관부속 상당직관 길이', '90° · 45° 엘보 · 분류 · 직류 티 · 게이트 · 볼 · 앵글 · 체크 밸브 — 관경별 표(계산식 안내 「관부속 참고」 탭)'],
 ['전달계수 · 효율', f"K 전동기 직결 {D['TRANS_TYPE']['1']['k']} · 그 밖 {D['TRANS_TYPE']['2']['k']} · 효율은 사용자 입력(구경별 참고 40 ~ 70 %) — 제조사 성능곡선으로 확인"],
 ['HP 규격', '3 · 5 · 7.5 · 10 · 15 · 20 · 25 · 30 · 40 · 50 · 60 · 75 · 100 · 125 · 150 · 200 HP — 1 kW = 1.341 HP'],
], ['항목', '내용']))}
<h3 id="s4-7">4-7. v5.1.0 정정 ({DATE})</h3>
{BR(K(T([
 ['NFPC 109 판', '[소방청고시 제2025-25호, 2025. 12. 24. 타법개정]', '소방청고시 제2025-28호(2025. 12. 31. 일부개정, 2026. 3. 1. 시행)'],
 ['NFTC 109', '인용 없음', '국립소방연구원공고 제2026-9호(2026. 3. 1. 시행) — 헤더 · A4 · 계산식 안내'],
 ['조문 표기', '「제5조①③」 · 「제5조①④」', '제5조①3호 · ①4호'],
 ['350 L/min', '「고정」', '「이상」 기준 — 계산은 350 L/min'],
 ['유속 경고', '근거 없이 「유속 제한 ≤ 4 m/s」', '「참고 — NFTC 102 2.3.5 준용(옥외소화전 기준에는 없음)」'],
 ['강관 내경', 'KS D 3562 65A 62.7 mm · KS D 3507 65A 69.0 mm 등', 'KS 외경 − 2 × 두께(3562 65A 65.9 · 3507 65A 67.9 mm)'],
 ['압력 판정', '없음', 'S 토출압력 1.2 MPa(배관 재질) · T 최저 소화전 0.7 MPa(감압장치) · 최저 소화전 높이 입력'],
 ['참고값 표기', '근거 표기 없음', '안전율 · 올림 · 호스 · 관부속 · K · η · C = MANMIN 참고값'],
 ['이용방법 창 · 표기', '「⚙️ 조건 입력」 · 「📄 계산서」 · 「📱 모바일」 탭, 효율 자동 설정 · η가 「Η」로 보임', '실제 탭 이름 · 효율 직접 입력 · 대문자 변환 해제'],
 ['엔진', '계산이 화면 컴포넌트 안', '<code>hyd-engine</code> hydCalc 단일화 — 화면 · A4 · 검증 공용, 독립 구현 50,000건 대조 불일치 0'],
], ['항목', '기존', '정정'])))}
</section>""")

S.append(f"""<section class="ch" id="ch5"><h2><span class="n">05</span>실무 작업 방법</h2>
<h3 id="s5-1">5-1. 단계별 절차</h3>
<div class="svgbox">{FLOW_SVG}</div>
{K(T([
 ['① 설치 대상 · 배치', '소방시설법 시행령 별표 4 제1호사목 설치 대상 확인 · 각 부분 수평거리 40 m 이하로 소화전 배치 · 방수총 대상 여부'],
 ['② 개수 · 수원', '설치개수 → 2개 한도 · 수원 7 m³/개 · 다른 설비와 겸용이면 합산(제11조)'],
 ['③ 배관 경로', '펌프 → 옥외 매설 배관 → 가장 높은 · 먼 소화전까지 구간을 나누고 관부속 수량 집계'],
 ['④ 전양정 · 동력 · 압력', '실양정 · 마찰손실 · 호스 · 25 m → 전양정 · 동력 · 표준 HP · 토출압력 1.2 MPa 배관 · 최저 소화전 0.7 MPa 감압'],
 ['⑤ 기록', 'A4 계산서를 PDF · JPG로 남겨 소방설계도서 · 착공신고 서류에 첨부'],
], ['단계', '내용']))}
<h3 id="s5-2">5-2. 설계 · 승인 전 확인</h3>
{K(T([
 ['기준 시점', '건축허가 등 신청일 · 착공신고일에 따라 종전 기준 적용 여부(부칙 경과조치)'],
 ['펌프 선정', '정격점 · 체절 140 % · 150 % 유량 65 % — 제조사 성능곡선으로 확인'],
 ['배관 · 감압', '토출압력 1.2 MPa 이상이면 KS D 3562 등 · 0.7 MPa 넘는 소화전은 감압장치 — 앱 판정(추정)을 성능곡선으로 다시 확인'],
 ['참고값', '호스 손실 · 관부속 상당길이 · 효율 · 안전율은 사용 제품 · 사무소 기준으로 바꿔 넣기'],
], ['항목', '확인']))}
</section>""")

S.append(f"""<section class="ch" id="ch6"><h2><span class="n">06</span>문제 해결·FAQ</h2>
{K(T([
 ['소화전을 6개 넣었는데 2개로 계산돼요', '옥외소화전은 설치개수가 2개 이상이면 2개로 계산합니다(제4조① · 제5조①3호)'],
 ['수원이 예전 판과 같은데 양정이 조금 달라졌어요', 'KS 강관 내경을 KS 외경 · 두께로 다시 계산했습니다(<a href="#s4-5">4-5</a>)'],
 ['「배관 부적합」 · 「감압장치 필요」가 떠요', '토출압력 1.2 MPa 이상이면 KS D 3562 등으로 바꾸고, 감압장치 필요면 표시된 높이 미만 호스접결구에 감압장치를 두십시오 — 계산값은 그대로입니다'],
 ['유속 ⚠는 지켜야 하나요', '옥외소화전 기준에는 유속 규정이 없습니다 — 옥내소화전 기준(4 m/s)을 참고로 보여 주는 것입니다'],
 ['안전율 10 %는 꼭 넣어야 하나요', '기준에 없는 MANMIN 참고값입니다. 사무소 기준에 맞게 해석하되 계산서의 「참고값」 표기를 함께 남기십시오'],
 ['화면이 예전 판이에요', '새로 고침(Ctrl+F5) 또는 앱을 닫았다 다시 여십시오'],
], ['증상', '해결']))}
</section>""")

def inrow(nm, I):
    s_ = I['sys']
    segs = ' · '.join(f"{g['dia']}A {g['flow']}L/min {g['len']:g} m" for g in I['segs'])
    return [nm, f"소화전 {s_['hydrants']}개 · 실양정 {s_['actualHead']:g} m · 최저 소화전 {s_['lowHead']:g} m · {H[str(s_['hoseType'])]['label']} {s_['hoseLen']} m · {P[s_['pipeType']]['shortLabel']} · {s_['pumpDia']}A · η {s_['pumpEff']} %", segs]
def rrow(nm, R):
    return [nm, str(R['A']), str(R['Clpm']), f3(R['D']), f3(R['F']), str(R['J']), f"{R['Php']:g}", f3(R['Pdis']), f3(R['Plow'])]
S.append(f"""<section class="ch" id="ch7"><h2><span class="n">부록</span></h2>
<h3 id="a1">A1. 예제 입력값</h3>
{BR(K(T([inrow('예제 A', IA), inrow('예제 B', IB), inrow('예제 C', IC)], ['예제', '조건', '배관 구간'])))}
<h3 id="a2">A2. 예제 결과</h3>
{BR(T([rrow('예제 A', A), rrow('예제 B', Bx), rrow('예제 C', C)], ['예제', '개수', '토출량(L/min)', '수원(m³)', 'h₂(m)', '전양정(m)', 'HP', '토출압(MPa)', '최저 방수압(MPa)'], num_cols=(1, 2, 3, 4, 5, 6, 7, 8)))}
<p>예제 C는 최저 소화전 방수압이 0.7 MPa를 넘어 펌프 기준 {f1(C['hStar'])} m 미만 호스접결구에 감압장치를 검토합니다.</p>
<h3 id="a3">A3. 버전 변경 내역</h3>
{K(T([
 [f'Ver-5.1 · v5.1.0 ({DATE})', 'NFPC 109(제2025-28호) · NFTC 109(제2026-9호) 원문 대조 근거 정정, KS 강관 내경, 압력 판정(1.2 MPa 배관 · 0.7 MPa 감압), MANMIN 참고값 표기, 계산 엔진 단일화, 탭 막대 「📘 매뉴얼」 · 사용자 매뉴얼(<a href="#s4-7">4-7</a>)'],
 ['Ver-5.0 (2026-09)', 'MANMIN 디자인 통일(헤더 · 탭 · 요약 바 · A4 · JPG 저장), PWA'],
], ['버전', '내용']))}
<h3 id="a4">A4. 용어</h3>
{BR(K(T([
 ['호스접결구', '옥외소화전에서 호스를 연결하는 구 — 지면에서 0.5 ~ 1 m(제6조①2호)'],
 ['방수총', '대량의 물을 멀리 방사하는 노즐 장치 — 특수가연물 750배 이상 공장 · 창고에 설치(제6조①3호)'],
 ['전양정', '펌프가 내야 하는 전체 수두 — 실양정 + 마찰손실 + 노즐 방수압 환산수두'],
 ['상당직관', '관부속의 손실을 같은 지름 직관 길이로 바꾼 값'],
 ['체절운전', '토출 측 밸브를 닫고 펌프를 돌리는 성능시험(제5조①6호)'],
], ['용어', '뜻'])))}
</section>""")

html = render(title=f'{APP} 사용자 매뉴얼 {VER} · MANMIN',
              desc=f'{APP} MANMIN {VER} 사용자 매뉴얼 — 화면 기능, NFPC 109 · NFTC 109 해설, 실무 작업 방법',
              eyebrow='MANMIN ENGINEERING · USER MANUAL', h1=f'{APP} 사용자 매뉴얼',
              sub='수원 → 토출량 → 배관 · 호스 마찰손실 → 전양정 → 압력 판정 → 전동기 동력 → A4 계산서', ver=VER, date=DATE, app_name=APP,
              pdf=PDF, toc=TOC, sections=S, foot_note='NFPC 109 (소방청고시 제2025-28호) · NFTC 109 (국립소방연구원공고 제2026-9호)')
html = html.replace('화면 대응 개정 2026-10-12', '화면 대응 개정 ' + DATE)
open(os.path.join(B, 'index.html'), 'w', encoding='utf-8').write(html)
print('manual ok', len(html))
