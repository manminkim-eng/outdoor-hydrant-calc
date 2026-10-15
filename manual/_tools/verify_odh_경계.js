// 옥외소화전 v5.1.0 경계값 시험 — 1.2 MPa(NFTC 109 2.3.3.2 · NFPC 109 제6조③) · 0.7 MPa(제5조①3호 단서)
// usage: node verify_odh_경계.js <index.html> [치환 전] [치환 후]  (오류 주입 시험용 치환)
const fs=require('fs');let s=fs.readFileSync(process.argv[2],'utf8');const a=s.indexOf('<script id="hyd-engine">')+24;let e=s.slice(a,s.indexOf('</script>',a));
if(process.argv[3]) e=e.replace(process.argv[3],process.argv[4]);
var window=globalThis;eval(e);
const base={hydrants:2,hoseLen:30,hoseType:2,transType:1,pumpDia:100,pumpEff:60};
const T=[];
for(const [E,pt,hL,expOK,expPRV] of [[84.7,'SCH10',49.4,true,true],[84.8,'SCH10',49.4,false,true],[84.8,'SCH40',49.4,true,true],[84.7,'SCH10',49.5,true,false],[84.8,'STS',0,false,true]]){
 const c=hydCalc({...base,actualHead:E,pipeType:pt,lowHead:hL},[]);T.push([E,pt,hL,c.J,c.Pdis.toFixed(4),c.pipePressOK,c.Plow.toFixed(4),c.needPRV,c.pipePressOK===expOK&&c.needPRV===expPRV?'✓':'✗']);}
console.log(T.map(r=>r.join(' | ')).join('\n'));
