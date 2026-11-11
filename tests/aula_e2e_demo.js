const {chromium}=require('playwright');
const U='http://localhost:8765/aula/index.html';
const toast=async p=>{await p.waitForSelector('#toast.show',{state:'attached',timeout:5000});return (await p.locator('#toast').innerText())};
async function llenar(p,d){
  for(const [k,v] of Object.entries(d)){const el=p.locator('#f_'+k);const tag=await el.evaluate(e=>e.tagName);
    if(tag==='SELECT')await el.selectOption(v);else await el.fill(v);}
}
const alumno=(o={})=>({nombres:'Ana María',apellidos:'Benítez Gómez',cedula:'4567890',fechaNac:'1995-03-14',sexo:'Femenino',departamento:'Central',ciudad:'Luque',telefono:'0981123456',email:'ana@ejemplo.com',clave:'Clave1234',clave2:'Clave1234',...o});
(async()=>{
const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1100,height:900}});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
p.on('dialog',d=>d.accept('docente@demo.local'));
await p.goto(U);await p.waitForSelector('#lf');
console.log('1 guest sin sidebar:',await p.evaluate(()=>getComputedStyle(document.querySelector('#side')).display),'| banner demo:',await p.locator('.note').first().innerText().then(t=>t.slice(0,20)));
// registro
await p.click('text=Crear cuenta');await p.waitForSelector('#rg');
await llenar(p,alumno({clave:'abcdefgh',clave2:'abcdefgh'}));await p.check('#f_ok');await p.click('#rg button[type=submit]');
console.log('2 clave débil →',await toast(p));
await p.waitForTimeout(4700);
await llenar(p,alumno({cedula:'12ab'}));await p.click('#rg button[type=submit]');
await llenar(p,alumno());await p.click('#rg button[type=submit]');
await p.waitForSelector('h1:has-text("Hola")');
console.log('4 registrado →',await p.locator('h1').innerText(),'| sidebar visible:',await p.evaluate(()=>getComputedStyle(document.querySelector('#side')).display));
// persistencia: marcar actividad
await p.goto(U+'#/sesion/1');await p.check('#chk_s1_ej');await p.waitForTimeout(800);
// perfil + cambio de clave
await p.goto(U+'#/perfil');await p.waitForSelector('#pf');
console.log('5 cédula bloqueada:',await p.locator('#f_cedula').getAttribute('readonly')!==null);
await p.fill('#f_ciudad','San Lorenzo');await p.click('#pf button[type=submit]');console.log('6',await toast(p));await p.waitForTimeout(4700);
await p.fill('#p0','Mala0000');await p.fill('#p1','Nueva5678');await p.fill('#p2','Nueva5678');await p.click('#cp button[type=submit]');console.log('7 clave actual mala →',await toast(p));await p.waitForTimeout(4700);
await p.fill('#p0','Clave1234');await p.fill('#p1','Nueva5678');await p.fill('#p2','Nueva5678');await p.click('#cp button[type=submit]');console.log('8',await toast(p));await p.waitForTimeout(4700);
// salir y volver a entrar
await p.click('#out3');await p.waitForSelector('#lf');
await p.fill('#le','ana@ejemplo.com');await p.fill('#lp','Clave1234');await p.click('#lf button[type=submit]');console.log('9 clave vieja →',await toast(p));await p.waitForTimeout(4700);
await p.fill('#lp','Nueva5678');await p.click('#lf button[type=submit]');await p.waitForSelector('h1:has-text("Hola")');
await p.goto(U+'#/sesion/1');console.log('10 progreso persistido:',await p.locator('#chk_s1_ej').isChecked());
// recuperación
await p.click('#logout');await p.waitForSelector('#lf');await p.click('#olv');await p.fill('#re','ana@ejemplo.com');await p.click('#rf button');
await p.waitForFunction(()=>document.querySelector('#rmsg').textContent.includes('Temp'));
const tmp=(await p.locator('#rmsg').innerText()).match(/Temp\d+x/)[0];console.log('11 recuperación demo, temporal generada');
await p.fill('#le','ana@ejemplo.com');await p.fill('#lp',tmp);await p.click('#lf button[type=submit]');await p.waitForSelector('h1:has-text("Hola")');console.log('12 ingreso con clave temporal OK');
await p.click('#logout');await p.waitForSelector('#lf');
// cédula duplicada
await p.goto(U+'#/registro');await llenar(p,alumno({nombres:'Otra',email:'otra@ejemplo.com'}));await p.check('#f_ok');await p.click('#rg button[type=submit]');
console.log('13 cédula duplicada →',await toast(p));await p.waitForTimeout(4700);
console.log('   queda en "completar registro":',await p.locator('h1').innerText());
await p.click('#out2');await p.waitForSelector('#lf');
// docente
await p.goto(U+'#/registro');await llenar(p,alumno({nombres:'Prof',apellidos:'Docente',cedula:'1111111',email:'docente@demo.local'}));await p.check('#f_ok');await p.click('#rg button[type=submit]');
await p.waitForSelector('h1:has-text("Hola")');
await p.goto(U+'#/docente');await p.waitForSelector('tbody tr');
console.log('14 docente ve alumnos:',await p.locator('tbody tr').count(),'(incluye su propio perfil)');
await p.locator('tr:has-text("Benítez") input[data-id=s1_ej]').fill('4.5');await p.waitForTimeout(1000);
await p.screenshot({path:'/tmp/aula_docente.png'});
await p.click('#logout');await p.waitForSelector('#lf');
await p.fill('#le','ana@ejemplo.com');await p.fill('#lp',tmp);await p.click('#lf button[type=submit]');await p.waitForSelector('h1:has-text("Hola")');
await p.goto(U+'#/notas');console.log('15 alumno ve nota oficial:',(await p.locator('tr:has-text("Ejercicio S1")').innerText()).replace(/\s+/g,' '));
await p.goto(U+'#/docente');console.log('16 alumno no accede al panel:',await p.locator('h1').innerText());
console.log('errores JS:',errs);
await b.close();})();
