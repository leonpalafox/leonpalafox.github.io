import fs from 'node:fs';
import assert from 'node:assert/strict';
const targets=await (await fetch('http://127.0.0.1:9223/json/list')).json();
const ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);
await new Promise(r=>ws.onopen=r);
let id=0;const pending=new Map();const errors=[];
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text+': '+m.params.exceptionDetails.exception?.description);};
const send=(method,params={})=>new Promise((resolve,reject)=>{pending.set(++id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
const evaluate=async expression=>(await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true})).result.value;
await send('Page.enable');await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
await send('Page.navigate',{url:'http://127.0.0.1:4322/'});
await new Promise(r=>setTimeout(r,500));
const results=[];
for(const per of ['s','d']) for(const dom of ['sci','read','math']) for(const sigOnly of [false,true]){
 const result=await evaluate(`(()=>{
 document.getElementById('p-${per}').click();document.getElementById('d-${dom}').click();
 const cb=document.getElementById('sigonly');if(cb.checked!==${sigOnly})cb.click();
 const data=JSON.parse(document.getElementById('pisa-data').textContent);
 const values=data.rows.filter(r=>r['${per}']['${dom}']);
 const up=values.filter(r=>r['${per}']['${dom}'][1] && r['${per}']['${dom}'][0]>0).length;
 const dn=values.filter(r=>r['${per}']['${dom}'][1] && r['${per}']['${dom}'][0]<0).length;
 const stats=[...document.querySelectorAll('.tile .v')].map(e=>e.textContent);
 const eligible=values.filter(r=>!${sigOnly} || r['${per}']['${dom}'][1]).sort((a,b)=>b.evidence['${dom}']['${per}'].value-a.evidence['${dom}']['${per}'].value);
 const names=id=>[...document.querySelectorAll('#'+id+' .nm')].map(e=>e.textContent.split(' *').join('').split(' (NS)').join(''));
 const partialPaths=[...document.querySelectorAll('path.geo[aria-label]')].filter(e=>/^(B-S-J-Z|Ukrainian regions|Dushanbe|Kurdistan Region)/.test(e.getAttribute('aria-label')));
 return {stats,expected:[up,dn,values.length-up-dn,91-values.length],gains:names('gainers'),expectedGains:eligible.filter(r=>r.evidence['${dom}']['${per}'].value>0).slice(0,10).map(r=>r.name),losses:names('losers'),expectedLosses:eligible.filter(r=>r.evidence['${dom}']['${per}'].value<0).reverse().slice(0,10).map(r=>r.name),regionalNeutral:partialPaths.every(e=>e.style.fill==='var(--nodata)'),rows:document.querySelectorAll('#tbody tr').length};})()`);
 assert.deepEqual(result.stats.slice(1).map(Number),result.expected);assert.deepEqual(result.gains,result.expectedGains);assert.deepEqual(result.losses,result.expectedLosses);assert.equal(result.regionalNeutral,true);assert.equal(result.rows,91);
 results.push({per,dom,sigOnly,status:'PASS'});
}
const interaction=await evaluate(`(()=>{
 const b=[...document.querySelectorAll('#thead-row button')].find(e=>e.textContent.startsWith('Reading 2025'));b.click();
 [...document.querySelectorAll('#thead-row button')].find(e=>e.textContent.startsWith('Reading 2025')).click();
 const last=document.querySelector('#tbody tr:last-child td').textContent;
 document.getElementById('zin').click();const zoom=document.querySelector('#map > g > g').getAttribute('transform');
 document.getElementById('zreset').click();const reset=document.querySelector('#map > g > g').getAttribute('transform');
 const marker=[...document.querySelectorAll('.mk')].find(e=>e.getAttribute('aria-label').startsWith('Ukrainian'));marker.focus();
 const tip=document.getElementById('tip').textContent;
 marker.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));
 return {last,zoom,reset,tip,hidden:!document.getElementById('tip').classList.contains('on')};})()`);
assert.equal(interaction.last,'Uzbekistan');assert.ok(interaction.zoom.includes('1.500'));assert.ok(interaction.reset.includes('1.000'));assert.ok(interaction.tip.includes('17'));assert.equal(interaction.hidden,true);
for(const theme of ['light','dark']){
 await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-color-scheme',value:theme}]});
 await send('Page.navigate',{url:'http://127.0.0.1:4322/'});await new Promise(r=>setTimeout(r,300));
 await evaluate(fs.readFileSync(process.env.AXE_PATH || '/tmp/site-axe.min.js','utf8'));
 const axe=await evaluate(`axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}}).then(r=>r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})))`);
 results.push({theme,accessibility:axe});
 const shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true});fs.writeFileSync('audit/'+theme+'-1440.png',Buffer.from(shot.data,'base64'));
}
assert.deepEqual(errors,[]);
fs.writeFileSync('audit/browser-checks.json',JSON.stringify({results,interaction,errors},null,2));
console.log(JSON.stringify(results));ws.close();
