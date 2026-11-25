// Capture current source components in the existing isolated atlas laboratory.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
const skill=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const atlas=path.join(skill,'assets/atlas'),out=path.join(atlas,'audit-assets');fs.mkdirSync(out,{recursive:true});
const env={};env.window=env;
for(const name of ['motion-specs.js','cases.js','style-audit-data.js'])vm.runInNewContext(fs.readFileSync(path.join(atlas,name),'utf8'),env);
const data=env.CHLORA_STYLE_AUDIT,cases=env.UI_CASES;
const requested=process.argv[3]?new Set(process.argv[3].split(',')):null;
if(requested)for(const id of requested)if(!data.samples[id])throw Error('Unknown sample '+id);
const playwrightPath=process.env.CHLORA_PLAYWRIGHT_PATH||path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {webkit}=createRequire(import.meta.url)(fs.existsSync(playwrightPath)?playwrightPath:'playwright');
const browser=await webkit.launch({headless:true}),page=await browser.newPage({viewport:{width:1120,height:760},deviceScaleFactor:2});page.setDefaultTimeout(3500);
const errors=[],records=[];page.on('pageerror',e=>errors.push(String(e)));
const base=process.argv[2]||'http://127.0.0.1:17869';
// Expose an already-existing source function in the served test copy only.
// The original product and frozen atlas files are not edited by this route.
await page.route('**/source-ui/lab.html?**',async route=>{
 let html=fs.readFileSync(path.join(atlas,'source-ui/lab.html'),'utf8');
 html=html.replace('window.chloraUiLabSource={','window.chloraUiLabSource={showForm:showForm,showMenu:showMenu,');
 await route.fulfill({body:html,contentType:'text/html'});
});
for(const s of Object.values(data.samples).filter(s=>!requested||requested.has(s.id))){
 const row={id:s.id,caseId:s.caseId,selector:s.selector,state:s.state,label:s.label};
 try{
  const c=cases.find(c=>c.id===s.caseId);if(!c)throw Error('Missing case '+s.caseId);
  if(s.full&&!s.fragment){
   const source=path.join(atlas,'previews',s.caseId+'.jpg');if(!fs.existsSync(source))throw Error('Missing reviewed preview');
   row.file='previews/'+s.caseId+'.jpg';row.kind=s.nativeReplay?'source-parameter-replay':'existing-source-page';row.width=1120;row.height=760;
  }else{
   await page.goto(base+'/source-ui/lab.html?'+new URLSearchParams({kind:c.kind,variant:c.variant,theme:'light'}));
   await page.waitForFunction(()=>window.labReady||window.labError,null,{timeout:9000});
   const labError=await page.evaluate(()=>window.labError);if(labError)throw Error(labError);
   await page.waitForTimeout(550);
   // Logical 100% for comparable control crops. Dialogs are already screen-fixed.
   await page.evaluate(()=>document.getElementById('graphWorld')?.style.setProperty('transform','translate(0,0) scale(1)','important'));
   if(s.fragment==='lfo-mapping')await page.evaluate(()=>{
    document.querySelector('.app').style.display='none';
    const el=document.createElement('div');el.className='graph-lfo-wire-hint audit-lfo-hint';el.style.cssText='position:fixed;display:flex;left:200px;top:220px;opacity:1;transform:none';document.body.append(el);
    window.auditConnection={depth:.5,mode:'remote',minimum:.2,maximum:.8};
    window.auditMapping=ChloraLfoUI.wireDepthControl(el,{connection:()=>auditConnection,parameterName:()=> 'Gain',mapping(c,next){Object.assign(c,next);},commit(c,value){c.depth=value;}});
   });
   if(s.fragment==='context-form'||s.fragment==='context-validation')await page.evaluate(invalid=>{
    chloraUiLabSource.showForm(200,180,'Stack dimensions',[{name:'count',label:'Instances',value:3,min:1,max:128,step:1},{name:'width',label:'Channels per instance',value:2,min:1,max:2,step:1}],()=>{},invalid?()=>({field:'count',message:'Disconnect Stack I/O before changing its channel count.'}):undefined);
   },s.fragment==='context-validation');
   if(s.fragment==='context-validation')await page.locator('#ctxDialog [data-ok]').click();
   if(s.fragment==='brand-menu')await page.evaluate(()=>{
    chloraUiLabSource.showMenu(200,180,[{label:'Settings',run(){}},{label:'Cheat Sheet',run(){}},{label:'About Chlora',run(){}}],'Chlora');document.getElementById('ctxMenu').classList.add('ctx-brand-menu');
   });
   if(s.fragment==='monitor-choice'){
    await page.evaluate(()=>{const r=labState.fileGraph.monitorNodes[0];r.listeningLayouts.push({id:'wide',name:'Example 4 CH',channels:4,roles:['1','2','3','4']});labPublish();});
    await page.locator('[data-fg-monitor-layout]').click();
   }
   if(s.fragment==='playback-loop'){
    await page.evaluate(()=>{Object.assign(labState.fileGraph.sources[0].playback,{loopEnabled:true,loopStartSeconds:2,loopEndSeconds:6});labPublish();});
    s.selector='.fgp-source-editor button[aria-pressed]';row.selector=s.selector;
   }
   if(s.fragment==='instance-menu')await page.locator('#instanceToggle').click();
   if(['sm-console','sm-source','sm-round','sm-router'].includes(s.id))await page.evaluate(id=>{
    if(id==='sm-console')labState.channels[0].soloed=true;
    if(id==='sm-source')labState.fileGraph.sources[0].solos[0]=true;
    if(id==='sm-round')labState.graphNodes[0].channelStates[0].soloed=true;
    if(id==='sm-router')labState.graphNodes[0].routerInputControls[0]=1;
    labPublish();
   },s.id);
   if(s.id==='sm-ir')await page.locator('.ir-editor-solo').first().click();
   if(s.state==='edit-strip')await page.locator('.lab-stage .channel-db').first().click();
   if(s.state==='edit-distance')await page.locator('[data-ir-distance-depth]').click();
   if(s.state==='invalid-align'){
    const input=page.locator('.graph-channel-number').first();await input.fill('bad');await input.press('Enter');
    row.afterInvalid=await input.inputValue();
   }
   if(s.state==='invalid-lfo'){
    await page.locator('.graph-lfo-range input').first().focus();
    await page.locator('.graph-lfo-range input').first().fill('120');
    row.ariaInvalid=await page.locator('.graph-lfo-range input').first().getAttribute('aria-invalid');
    row.invalidComputed=await page.locator('.graph-lfo-range input').first().evaluate(e=>({decoration:getComputedStyle(e).textDecoration,focusVisible:e.matches(':focus-visible')}));
   }
   let selector=s.selector;
   if(s.full&&s.fragment==='instance-menu')selector='#instanceMenu';
   const target=page.locator(selector).first();await target.waitFor({state:'visible'});await target.scrollIntoViewIfNeeded();
   if(s.state==='focus'){await page.keyboard.press('Tab');await page.locator(s.focusSelector||selector).first().focus();}
   if(s.state==='hover')await page.locator(s.hoverSelector||selector).first().hover();
   if(s.state==='pressed'){await target.hover();await page.mouse.down();}
   if(s.state==='selected-plugin')await target.click();
   await page.waitForTimeout(s.state==='pressed'?45:180);
   row.computed=await target.evaluate(e=>{const c=getComputedStyle(e);return {font:c.font,color:c.color,background:c.backgroundColor,border:c.border,borderRadius:c.borderRadius,outline:c.outline,textDecoration:c.textDecoration,boxShadow:c.boxShadow,textShadow:c.textShadow,transform:c.transform,transition:c.transition,width:c.width,height:c.height};});
   if(s.id.startsWith('sm-'))row.soloState=await target.evaluate(e=>[e,...e.querySelectorAll('button')].map(b=>({text:b.textContent,on:b.classList.contains('on'),pressed:b.getAttribute('aria-pressed')})));
   const box=await target.boundingBox();if(!box)throw Error('No rendered target bounds');
   const pad=10,x=Math.max(0,box.x-pad),y=Math.max(0,box.y-pad),width=Math.min(1120-x,box.width+pad*2),height=Math.min(760-y,box.height+pad*2);
   if(width<2||height<2)throw Error('Target outside viewport');
   await page.screenshot({path:path.join(out,s.id+'.png'),clip:{x,y,width,height},scale:'css'});
   if(s.state==='pressed')await page.mouse.up();
   row.file='audit-assets/'+s.id+'.png';row.kind='source-control-crop';row.width=width;row.height=height;
   row.titleAttributes=await page.locator('[title]').count();
  }
  row.passed=true;
 }catch(error){row.passed=false;row.error=String(error.message||error);console.log('FAIL '+s.id+' '+row.error.slice(0,180));}
 records.push(row);if(row.passed)console.log('OK '+s.id);
}
await browser.close();
const report={date:'2026-10-29',engine:'Headless WebKit',claim:'Source CSS/DOM crops and simulated-state components only; no native/audio/DAW claim',groups:data.groups.length,records,errors,passed:records.every(r=>r.passed)&&!errors.length};
const reportPath=path.join(atlas,'qa',requested?'style-audit-targeted.json':'style-audit-captures.json');
fs.writeFileSync(reportPath,JSON.stringify(report,null,2)+'\n');
let existing={};const mediaPath=path.join(atlas,'style-audit-media.json');if(fs.existsSync(mediaPath))existing=JSON.parse(fs.readFileSync(mediaPath,'utf8'));
for(const row of records)existing[row.id]=row;
fs.writeFileSync(mediaPath,JSON.stringify(existing,null,2)+'\n');
console.log('STYLE_AUDIT '+(report.passed?'PASS':'FAIL')+' '+records.length+' samples');
if(!report.passed)process.exitCode=1;
