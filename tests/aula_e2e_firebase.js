const {chromium}=require('playwright');const fs=require('fs');
const U='http://localhost:8765/aula/index.html', AUTH='http://127.0.0.1:9099', FS='http://127.0.0.1:8080', PRJ='demo-cvd';
const dataJs=fs.readFileSync(require('path').join(__dirname, '..', 'site', 'aula', 'data.js'),'utf8');
const mod=dataJs.replace(/^window\.CURSO=/,'').replace(/;$/,'');const cur=JSON.parse(mod);
cur.config.firebase={apiKey:'fake-key',projectId:PRJ,authDomain:'localhost',appId:'1:1:web:1'};
const newData='window.CURSO='+JSON.stringify(cur)+';';
const toast=async p=>{await p.waitForSelector('#toast.show',{timeout:8000});return (await p.locator('#toast').innerText())};
const idle=p=>p.waitForTimeout(4700);
async function llenar(p,d){for(const [k,v] of Object.entries(d)){const el=p.locator('#f_'+k);if(await el.evaluate(e=>e.tagName)==='SELECT')await el.selectOption(v);else await el.fill(v);}}
const alumno=(o={})=>({nombres:'Ana María',apellidos:'Benítez Gómez',cedula:'4567890',fechaNac:'1995-03-14',sexo:'Femenino',departamento:'Central',ciudad:'Luque',telefono:'0981123456',email:'ana@ejemplo.com',clave:'Clave1234',clave2:'Clave1234',...o});
const oob=async(email,tipo)=>{const j=await (await fetch(`${AUTH}/emulator/v1/projects/${PRJ}/oobCodes`)).json();return j.oobCodes.filter(c=>c.email===email&&c.requestType===tipo).pop();};
const verificar=async email=>{const c=await oob(email,'VERIFY_EMAIL');await fetch(c.oobLink);};
const token=async(email,pw)=>(await (await fetch(`${AUTH}/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=fake`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({email,password:pw,returnSecureToken:true})})).json());
const fsr=(m,path,tok,body)=>fetch(`${FS}/v1/projects/${PRJ}/databases/(default)/documents/${path}`,{method:m,headers:{Authorization:'Bearer '+tok,'content-type':'application/json'},body:body?JSON.stringify(body):undefined}).then(r=>r.status);
const campos=o=>({fields:Object.fromEntries(Object.entries(o).map(([k,v])=>[k,typeof v==='string'?{stringValue:v}:{mapValue:{fields:{fecha:{stringValue:'x'}}}}]))});
(async()=>{
await fetch(`${AUTH}/emulator/v1/projects/${PRJ}/accounts`,{method:'DELETE'});await fetch(`${FS}/emulator/v1/projects/${PRJ}/databases/(default)/documents`,{method:'DELETE'});
const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1100,height:900}});
await ctx.addInitScript(()=>{window.__CVD_EMULATOR__={auth:'http://127.0.0.1:9099',fsHost:'127.0.0.1',fsPort:8080};});
await ctx.route('**/aula/data.js',r=>r.fulfill({contentType:'application/javascript',body:newData}));
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
await p.goto(U);await p.waitForSelector('#lf');console.log('modo real: banner demo ausente =',await p.locator('.note').count()===0);
// 1 registro + verificación
await p.click('text=Crear cuenta');await llenar(p,alumno());await p.check('#f_ok');await p.click('#rg button[type=submit]');
await p.waitForSelector('h1:has-text("Verificá tu correo")');console.log('1 registro → pide verificar correo');
await verificar('ana@ejemplo.com');await p.click('#vok');await p.waitForSelector('h1:has-text("Hola")');console.log('2 verificado →',await p.locator('h1').innerText());
// 3 progreso y persistencia tras recargar
await p.goto(U+'#/sesion/1');await p.check('#chk_s1_ej');await p.waitForTimeout(1200);await p.reload();await p.waitForSelector('#chk_s1_ej');
console.log('3 sesión y progreso persisten tras recargar:',await p.locator('#chk_s1_ej').isChecked());
// 4 cédula duplicada desde otro contexto
const c2=await b.newContext();await c2.addInitScript(()=>{window.__CVD_EMULATOR__={auth:'http://127.0.0.1:9099',fsHost:'127.0.0.1',fsPort:8080};});await c2.route('**/aula/data.js',r=>r.fulfill({contentType:'application/javascript',body:newData}));
const q=await c2.newPage();q.on('pageerror',e=>errs.push(e.message));
await q.goto(U+'#/registro');await llenar(q,alumno({nombres:'Otra',email:'otra@ejemplo.com'}));await q.check('#f_ok');await q.click('#rg button[type=submit]');
console.log('4 cédula duplicada (reglas) →',await toast(q));
// 5 recuperación
await p.click('#logout');await p.waitForSelector('#lf');await p.click('#olv');await p.fill('#re','ana@ejemplo.com');await p.click('#rf button');
await p.waitForFunction(()=>document.querySelector('#rmsg').textContent.length>5);
const rc=await oob('ana@ejemplo.com','PASSWORD_RESET');console.log('5 correo de recuperación generado:',!!rc);
const rr=await fetch(`${AUTH}/identitytoolkit.googleapis.com/v1/accounts:resetPassword?key=fake`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({oobCode:rc.oobCode,newPassword:'Reset9999'})});console.log('   restablecer con el enlace:',rr.status);
await p.fill('#le','ana@ejemplo.com');await p.fill('#lp','Clave1234');await p.click('#lf button[type=submit]');console.log('6 clave anterior rechazada →',await toast(p));await idle(p);
await p.fill('#lp','Reset9999');await p.click('#lf button[type=submit]');await p.waitForSelector('h1:has-text("Hola")');console.log('7 ingreso con clave nueva OK');
// 8 cambiar clave en la UI
await p.goto(U+'#/perfil');await p.waitForSelector('#cp');await p.fill('#p0','Reset9999');await p.fill('#p1','Final12345');await p.fill('#p2','Final12345');await p.click('#cp button[type=submit]');console.log('8 cambio de clave →',await toast(p));
console.log('   token con clave nueva:',!!(await token('ana@ejemplo.com','Final12345')).idToken);
// docente
await fsr('POST','docentes?documentId=docente%40demo.local','owner',{fields:{activo:{booleanValue:true}}});
const d=await b.newContext({viewport:{width:1300,height:900}});await d.addInitScript(()=>{window.__CVD_EMULATOR__={auth:'http://127.0.0.1:9099',fsHost:'127.0.0.1',fsPort:8080};});await d.route('**/aula/data.js',r=>r.fulfill({contentType:'application/javascript',body:newData}));
const t=await d.newPage();t.on('pageerror',e=>errs.push(e.message));
await t.goto(U+'#/registro');await llenar(t,alumno({nombres:'Prof',apellidos:'Docente',cedula:'1111111',email:'docente@demo.local'}));await t.check('#f_ok');await t.click('#rg button[type=submit]');
await t.waitForSelector('h1:has-text("Verificá")');await verificar('docente@demo.local');await t.click('#vok');await t.waitForSelector('h1:has-text("Hola")');
await t.goto(U+'#/docente');await t.waitForSelector('tbody tr');console.log('9 docente ve estudiantes:',await t.locator('tbody tr').count(),'→',(await t.locator('tbody tr').first().innerText()).split('\n')[0]);
await t.locator('tr:has-text("Benítez") input[data-id=s1_ej]').fill('4.5');await t.waitForFunction(()=>document.querySelector('#toast').textContent.includes('Nota guardada'),null,{timeout:8000});console.log('10 nota guardada → Nota guardada ✔');
await t.screenshot({path:'/tmp/aula_docente.png'});
await p.goto(U+'#/notas');await p.waitForSelector('table');console.log('11 alumno ve su nota:',(await p.locator('tr:has-text("Ejercicio S1")').innerText()).replace(/\s+/g,' ').slice(-12));
await p.goto(U+'#/docente');console.log('12 alumno en #/docente:',await p.locator('h1').innerText());
// REGLAS: ataques directos por REST
const A=await token('ana@ejemplo.com','Final12345'), O=await token('docente@demo.local','Clave1234');
const ua=A.localId; const otraUid=(await token('otra@ejemplo.com','Clave1234')).localId;
console.log('--- reglas de seguridad (esperado: 403 = bloqueado, 200 = permitido)');
console.log(' alumno lee su perfil           :',await fsr('GET','usuarios/'+ua,A.idToken));
console.log(' alumno lee perfil de otra cuenta:',await fsr('GET','usuarios/'+otraUid,A.idToken));
console.log(' alumno lista todos los usuarios :',await fsr('GET','usuarios',A.idToken));
console.log(' alumno se pone nota (califs)    :',await fsr('PATCH','calificaciones/'+ua,A.idToken,{fields:{oficial:{mapValue:{fields:{s1_ej:{integerValue:'5'}}}}}}));
console.log(' alumno cambia su cédula         :',await fsr('PATCH','usuarios/'+ua+'?updateMask.fieldPaths=cedula',A.idToken,{fields:{cedula:{stringValue:'9999999'}}}));
console.log(' alumno se hace docente          :',await fsr('POST','docentes?documentId=ana%40ejemplo.com',A.idToken,{fields:{x:{booleanValue:true}}}));
console.log(' alumno lee lista de docentes    :',await fsr('GET','docentes',A.idToken));
console.log(' anónimo lee usuarios            :',await fsr('GET','usuarios/'+ua,'x'));
console.log(' docente lee perfil de alumno    :',await fsr('GET','usuarios/'+ua,O.idToken));
console.log(' docente escribe calificaciones  :',await fsr('PATCH','calificaciones/'+ua,O.idToken,{fields:{oficial:{mapValue:{fields:{s1_ej:{integerValue:'4'}}}}}}));
console.log(' docente lee cédulas (índice)    :',await fsr('GET','cedulas/4567890',O.idToken));
console.log('errores JS:',errs);
await b.close();})().catch(e=>{console.error('FALLÓ:',e.message);process.exit(1)});
