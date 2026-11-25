import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import vm from 'node:vm';
import {createRequire} from 'node:module';
const skill=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const atlas=path.join(skill,'assets/atlas');
const out=process.env.CHLORA_ATLAS_QA_OUT?path.resolve(process.env.CHLORA_ATLAS_QA_OUT):path.join(atlas,'qa'),previews=path.join(atlas,'previews');fs.mkdirSync(out,{recursive:true});fs.mkdirSync(previews,{recursive:true});
const scope={};scope.window=scope;
vm.runInNewContext(fs.readFileSync(path.join(atlas,'motion-specs.js'),'utf8'),scope);
vm.runInNewContext(fs.readFileSync(path.join(atlas,'cases.js'),'utf8'),scope);
const cases=scope.window.UI_CASES;
const playwrightPath=process.env.CHLORA_PLAYWRIGHT_PATH||path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {webkit}=createRequire(import.meta.url)(fs.existsSync(playwrightPath)?playwrightPath:'playwright');
const browser=await webkit.launch({headless:true});
const page=await browser.newPage({viewport:{width:1120,height:760}});
const errors=[],results=[];page.on('pageerror',e=>errors.push(String(e)));
const base=process.argv[2]||'http://127.0.0.1:17869';
const wanted=process.argv[3];
const selected=wanted?new Set(wanted.split(',')):null;
if(selected)for(const id of selected)if(!cases.some(c=>c.id===id))throw Error('Unknown case '+id);
for(const c of cases.filter(c=>!selected||selected.has(c.id))){
 let row={id:c.id,kind:c.kind};
 try{
 const theme=c.id.startsWith('theme-')?c.id.slice(6):'light';
 await page.goto(base+'/'+(c.historical?'history/20261029/source-ui/lab.html':'source-ui/lab.html')+'?'+new URLSearchParams({kind:c.kind,variant:c.variant,theme}));
 await page.waitForFunction(()=>window.labReady||window.labError,null,{timeout:10000});
 row=Object.assign(row,await page.evaluate(()=>({ready:labReady,error:window.labError||null,nodes:document.querySelectorAll('.graph-node').length,labStage:!!document.querySelector('.lab-stage'),text:document.body.innerText.slice(-250),size:{w:innerWidth,h:innerHeight},visibleControls:[...document.querySelectorAll('button,input,[role="slider"]')].filter(e=>e.getBoundingClientRect().width&&e.getBoundingClientRect().height).length})));
 if(row.error)throw Error(row.error);
 if(c.kind==='motion')await page.locator('[data-motion-time]').evaluate(el=>{el.value=String(Number(el.max)*.55);el.dispatchEvent(new Event('input',{bubbles:true}));});
 else await page.waitForTimeout(550);
 if(c.id==='source-playback'){await page.locator('.fgp-source-editor').waitFor({state:'visible',timeout:5000});await page.waitForFunction(()=>document.querySelector('.fgp-source-editor canvas')?.dataset.waveMode==='source',null,{timeout:5000});row.sourcePlaybackVisible=true;row.syntheticSourceWave=true;}
 if(c.id==='node-selected'&&!await page.locator('.graph-node.is-selected').count())throw Error('Selected node has no source selection class');
 if(c.id==='node-bypass'&&!await page.locator('.graph-node.is-node-bypassed').count())throw Error('Bypassed node has no source bypass class');
 if(c.kind==='preview'&&!await page.locator('.lab-stage .node-library-card').count())throw Error('Missing actual preview card');
 if(c.kind==='checkbox'){
   row.checkboxStates=await page.locator('.lab-stage input[type=checkbox]').evaluateAll(es=>es.map(e=>({checked:e.checked,disabled:e.disabled,mixed:e.indeterminate,paint:getComputedStyle(e).getPropertyValue('--chlora-check-level')})));
   if(row.checkboxStates.length!==4||row.checkboxStates.some(e=>e.mixed))throw Error('Invalid checkbox state matrix');
 }
 if(['ir-editor','command-material'].includes(c.id)){
   if(!await page.locator('.ir-editor').isVisible())throw Error('Missing current IR editor');
   if(await page.locator('.ir-editor button').allTextContents().then(ts=>ts.some(t=>t.trim()==='Fit')))throw Error('Fit remains in IR specimen');
 }
 await page.screenshot({path:path.join(previews,c.id+'.jpg'),type:'jpeg',quality:70});
 if(['node-source','node-monitor','node-snake','node-router','node-matrix','node-align','node-lfo','node-ir','node-stack','node-plugin'].includes(c.id)||wanted)await page.screenshot({path:path.join(out,c.id+'.png')});
 }catch(e){row.error=String(e);}
 results.push(row);console.log(c.id+' '+(row.error?'FAIL '+row.error.slice(0,160):'OK '+row.visibleControls));
}
await page.goto(base+'/index.html');await page.waitForTimeout(1000);await page.screenshot({path:path.join(out,'atlas-wide.png')});
await page.setViewportSize({width:760,height:900});await page.screenshot({path:path.join(out,'atlas-narrow.png')});
const report={engine:'Playwright WebKit headless',claim:'Source component mounting and artifact navigation only; simulated data, no native/DAW/audio claim',results,errors,passed:results.every(r=>!r.error)&&errors.length===0};
fs.writeFileSync(path.join(out,wanted?'report-'+wanted.replace(/[^a-z0-9-]/g,'_')+'.json':'report.json'),JSON.stringify(report,null,2)+'\n');
await browser.close();console.log('ATLAS '+(report.passed?'PASS':'FAIL'));
if(!report.passed)process.exitCode=1;
