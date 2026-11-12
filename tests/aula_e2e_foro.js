const {chromium}=require('playwright');const fs=require('fs');
const U='http://localhost:8765/aula/index.html', AUTH='http://127.0.0.1:9099', FS='http://127.0.0.1:8080', PRJ='demo-cvd';
const cur=JSON.parse(fs.readFileSync(require('path').join(__dirname, '..', 'site', 'aula', 'data.js'),'utf8').replace(/^window\.CURSO=/,'').replace(/;$/,''));
cur.config.firebase={apiKey:'fake',projectId:PRJ,authDomain:'localhost',appId:'1:1:web:1'};
const verificar=async email=>{const j=await (await fetch(`${AUTH}/emulator/v1/projects/${PRJ}/oobCodes`)).json();await fetch(j.oobCodes.filter(c=>c.email===email&&c.requestType==='VERIFY_EMAIL').pop().oobLink);};
async function llenar(p,d){for(const [k,v] of Object.entries(d)){const el=p.locator('#f_'+k);if(await el.evaluate(e=>e.tagName)==='SELECT')await el.selectOption(v);else await el.fill(v);}}
const per=(n,ap,ci,em)=>({nombres:n,apellidos:ap,cedula:ci,fechaNac:'1995-03-14',sexo:'Femenino',departamento:'Central',ciudad:'Luque',email:em,clave:'Clave1234',clave2:'Clave1234'});
const browser=chromium.launch();
async function usuario(b,datos){const ctx=await b.newContext({viewport:{width:1100,height:900}});await ctx.addInitScript(()=>{window.__CVD_EMULATOR__={auth:'http://127.0.0.1:9099',fsHost:'127.0.0.1',fsPort:8080};});
 await ctx.route('**/aula/data.js',r=>r.fulfill({contentType:'application/javascript',body:'window.CURSO='+JSON.stringify(cur)+';'}));
 await ctx.route('**/i.ytimg.com/**',r=>r.abort());
 const p=await ctx.newPage();p.on('pageerror',e=>errs.push(datos.email+': '+e.message));p.on('dialog',d=>d.accept());
 await p.goto(U+'#/registro');await p.waitForSelector('#rg');await llenar(p,datos);await p.check('#f_ok');await p.click('#rg button[type=submit]');
 await p.waitForSelector('h1:has-text("Verificá")');await verificar(datos.email);await p.click('#vok');await p.waitForSelector('h1:has-text("Hola")');return p;}
const errs=[];
(async()=>{
await fetch(`${AUTH}/emulator/v1/projects/${PRJ}/accounts`,{method:'DELETE'});await fetch(`${FS}/emulator/v1/projects/${PRJ}/databases/(default)/documents`,{method:'DELETE'});
await fetch(`${FS}/v1/projects/${PRJ}/databases/(default)/documents/docentes?documentId=prof%40x.com`,{method:'POST',headers:{Authorization:'Bearer owner','content-type':'application/json'},body:JSON.stringify({fields:{activo:{booleanValue:true}}})});
const b=await browser;
const ana=await usuario(b,per('Ana María','Benítez','1111111','ana@x.com')), beto=await usuario(b,per('Beto','Ruiz','2222222','beto@x.com')), prof=await usuario(b,per('Prof','Docente','3333333','prof@x.com'));
// 1 Ana crea tema
await ana.goto(U+'#/foros');await ana.waitForSelector('#fnew');console.log('1 foro vacío:',(await ana.locator('#flist').innerText()).slice(0,40));
await ana.click('#fnew');await ana.selectOption('#fm','2');await ana.fill('#ft','¿Cómo evito el overplotting con 50.000 puntos?');await ana.fill('#fc','Probé con alpha pero sigue saturado.\nMás info: https://seaborn.pydata.org/');await ana.click('#fform button[type=submit]');
await ana.waitForSelector('h1:has-text("overplotting")');console.log('2 tema creado → vista de hilo:',(await ana.locator('.post .muted').first().innerText()).replace(/\s+/g,' '),'| enlace clickeable:',await ana.locator('.ptxt a[href^="https://seaborn"]').count());
const url=ana.url();
// 3 Beto responde
await beto.goto(url);await beto.waitForSelector('#rform');await beto.fill('#rc','Usá hexbin o geom_bin2d, o reducí el tamaño del marcador.');await beto.click('#rform button[type=submit]');await beto.waitForSelector('.reply');
console.log('3 Beto respondió:',await beto.locator('.reply').count(),'respuesta | puede marcar solución (no es autor):',await beto.locator('[data-sol]').count()===0);
// 4 Ana marca solución
await ana.reload();await ana.waitForSelector('.reply');await ana.click('[data-sol]');await ana.waitForSelector('.reply.sol');console.log('4 Ana marcó la solución → resuelto:',await ana.locator('.tag.ok:has-text("resuelto")').count()>0);
// 5 lista y filtros
await beto.goto(U+'#/foros/2');await beto.waitForSelector('.fth');console.log('5 lista módulo 2:',await beto.locator('.fth').count(),'tema | respuestas:',(await beto.locator('.fcount').first().innerText()),'| resuelto:',await beto.locator('.fth .tag.ok').count());
await beto.goto(U+'#/foros/5');await beto.waitForSelector('#flist');console.log('   módulo 5 (otro):',(await beto.locator('#flist').innerText()).slice(0,26));
await beto.goto(U+'#/foros');await beto.fill('#fq','hexbin');console.log('   búsqueda "hexbin" (texto de respuesta, no del tema):',await beto.locator('.fth').count(),'→ busca solo en título/cuerpo');
await beto.fill('#fq','overplotting');console.log('   búsqueda "overplotting":',await beto.locator('.fth').count());
// 6 docente modera
await prof.goto(url);await prof.waitForSelector('[data-a="fijar"]');console.log('6 docente ve controles de moderación: fijar/cerrar/eliminar =',await prof.locator('[data-a]').allInnerTexts());
await prof.click('[data-a="fijar"]');await prof.waitForSelector('h1:has-text("📌")');await prof.click('[data-a="cerrar"]');await prof.waitForSelector('.tag.warn');
await prof.fill('#rc','x').catch(()=>{});console.log('   docente fijó y cerró el tema; botón Responder deshabilitado:',await prof.locator('#rform button[type=submit]').isDisabled());
await beto.goto(url);await beto.waitForSelector('.tag.warn');console.log('   Beto ve el tema cerrado: formulario de respuesta oculto =',await beto.locator('#rform').count()===0);
const ANA_UID=await ana.evaluate(async()=>{const fb=await import('/aula/vendor/firebase.js');return fb.getAuth().currentUser.uid;});
// 7 ataques a las reglas (SDK real, como Beto: estudiante)
const ataque=(p,codigo)=>p.evaluate(async ({codigo,tid,anaUid})=>{const fb=await import('/aula/vendor/firebase.js');const db=fb.getFirestore(),auth=fb.getAuth(),me=auth.currentUser.uid;const F=(...a)=>fb.doc(db,...a);
  const base={modulo:1,titulo:'tema de prueba',cuerpo:'x',autorUid:me,autorNombre:'Beto R.',respuestas:0,resuelto:false,fijado:false,cerrado:false,creado:fb.serverTimestamp(),actualizado:fb.serverTimestamp()};
  const ops={
   suplantar:()=>fb.addDoc(fb.collection(db,'foros'),{...base,autorUid:anaUid}),
   nacer_fijado:()=>fb.addDoc(fb.collection(db,'foros'),{...base,fijado:true}),
   titulo_corto:()=>fb.addDoc(fb.collection(db,'foros'),{...base,titulo:'ab'}),
   modulo_99:()=>fb.addDoc(fb.collection(db,'foros'),{...base,modulo:99}),
   fijar_ajeno:()=>fb.updateDoc(F('foros',tid),{fijado:true}),
   resolver_ajeno:()=>fb.updateDoc(F('foros',tid),{resuelto:false}),
   editar_ajeno:()=>fb.updateDoc(F('foros',tid),{titulo:'hackeado'}),
   inflar_contador:()=>fb.updateDoc(F('foros',tid),{respuestas:fb.increment(50)}),
   borrar_ajeno:()=>fb.deleteDoc(F('foros',tid)),
   respuesta_docente_falsa:()=>fb.addDoc(fb.collection(db,'foros',tid,'respuestas'),{cuerpo:'x',autorUid:me,autorNombre:'Beto R.',esDocente:true,solucion:false,creado:fb.serverTimestamp()}),
   respuesta_ya_solucion:()=>fb.addDoc(fb.collection(db,'foros',tid,'respuestas'),{cuerpo:'x',autorUid:me,autorNombre:'Beto R.',esDocente:false,solucion:true,creado:fb.serverTimestamp()}),
   respuesta_en_cerrado:()=>fb.addDoc(fb.collection(db,'foros',tid,'respuestas'),{cuerpo:'x',autorUid:me,autorNombre:'Beto R.',esDocente:false,solucion:false,creado:fb.serverTimestamp()}),
   poner_solucion_ajena:async()=>{const rs=await fb.getDocs(fb.collection(db,'foros',tid,'respuestas'));return fb.updateDoc(rs.docs[0].ref,{solucion:false});},
   editar_resp_propia:async()=>{const rs=await fb.getDocs(fb.collection(db,'foros',tid,'respuestas'));return fb.updateDoc(rs.docs[0].ref,{cuerpo:'editado'});},
  };
  try{await ops[codigo]();return 'PERMITIDO';}catch(e){return e.code||e.message;}},{codigo,tid:url.split('/foro/')[1],anaUid:ANA_UID});
console.log('7 intentos de abuso como estudiante (esperado: permission-denied):');
for(const c of ['suplantar','nacer_fijado','titulo_corto','modulo_99','fijar_ajeno','resolver_ajeno','editar_ajeno','inflar_contador','borrar_ajeno','respuesta_docente_falsa','respuesta_ya_solucion','respuesta_en_cerrado','poner_solucion_ajena','editar_resp_propia'])console.log('  ',c.padEnd(26),await ataque(beto,c));
// 8 usuario autenticado SIN perfil no puede leer
const sin=await (await fetch(`${AUTH}/identitytoolkit.googleapis.com/v1/accounts:signUp?key=fake`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({email:'sinperfil@x.com',password:'Clave1234',returnSecureToken:true})})).json();
console.log('8 cuenta sin perfil lee foros:',await fetch(`${FS}/v1/projects/${PRJ}/databases/(default)/documents/foros`,{headers:{Authorization:'Bearer '+sin.idToken}}).then(r=>r.status),'| sin sesión:',await fetch(`${FS}/v1/projects/${PRJ}/databases/(default)/documents/foros`).then(r=>r.status),'| con perfil (Beto) lista temas OK:',await beto.evaluate(async()=>{const fb=await import('/aula/vendor/firebase.js');return (await fb.getDocs(fb.collection(fb.getFirestore(),'foros'))).size;}));
// 9 docente elimina respuesta y tema
await prof.goto(url);await prof.waitForSelector('.reply');await prof.click('[data-del]');await prof.waitForFunction(()=>!document.querySelector('.reply'));console.log('9 docente eliminó la respuesta; contador =',await prof.locator('h2:has-text("respuesta")').innerText());
await prof.click('[data-a="borrar"]');await prof.waitForSelector('#fnew');console.log('   docente eliminó el tema → lista vacía:',(await prof.locator('#flist').innerText()).slice(0,34));
await prof.screenshot({path:'/tmp/aula_foro.png'});
console.log('errores JS:',errs);await b.close();})().catch(e=>{console.error('FALLÓ',e.message);process.exit(1)});
