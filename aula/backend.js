/* Capa de acceso a datos del aula. Dos implementaciones con la MISMA interfaz:
   - Firebase (Auth + Firestore): producción. Se activa si config.firebase.apiKey está definido.
   - Demo: todo en localStorage del navegador, solo para probar la interfaz (NO es seguro ni compartido).
   Colecciones Firestore: usuarios/{uid} · progreso/{uid} · calificaciones/{uid} · cedulas/{cedula} · docentes/{email} */

const ERR = {
  "auth/email-already-in-use": "Ese correo ya tiene una cuenta. Ingresá o recuperá tu contraseña.",
  "auth/invalid-credential": "Correo o contraseña incorrectos.",
  "auth/wrong-password": "Correo o contraseña incorrectos.",
  "auth/user-not-found": "Correo o contraseña incorrectos.",
  "auth/invalid-email": "El correo no es válido.",
  "auth/weak-password": "La contraseña es muy débil (mínimo 8 caracteres, con letras y números).",
  "auth/too-many-requests": "Demasiados intentos. Esperá unos minutos y volvé a intentar.",
  "auth/network-request-failed": "Sin conexión con el servidor. Revisá tu internet.",
  "auth/popup-closed-by-user": "Cerraste la ventana de Google antes de terminar.",
  "auth/popup-blocked": "El navegador bloqueó la ventana de Google. Permití las ventanas emergentes.",
  "auth/requires-recent-login": "Por seguridad, volvé a ingresar y repetí la operación.",
  "auth/operation-not-allowed": "Este método de ingreso no está habilitado en el servidor.",
  "auth/unauthorized-domain": "Este dominio no está autorizado en Firebase (Authentication → Configuración → Dominios autorizados).",
  "permission-denied": "No tenés permiso para esta operación (revisá las reglas de Firestore).",
  "cedula-duplicada": "Esa cédula ya está registrada. Si es tuya, ingresá con tu cuenta o contactá al docente.",
};
export const msgError = e => ERR[e?.code] || ERR[e?.message] || (e?.message && !/^Firebase/.test(e.message) ? e.message : "Ocurrió un error. Intentá de nuevo.");

/* ===================== FIREBASE ===================== */
async function crearFirebase(cfg) {
  const fb = await import("./vendor/firebase.js");
  const app = fb.initializeApp(cfg.firebase);
  const auth = fb.getAuth(app), db = fb.getFirestore(app);
  const emu = window.__CVD_EMULATOR__;
  if (emu) { fb.connectAuthEmulator(auth, emu.auth, { disableWarnings: true }); fb.connectFirestoreEmulator(db, emu.fsHost, emu.fsPort); }
  const U = u => u && ({ uid: u.uid, email: u.email, emailVerified: u.emailVerified, proveedor: u.providerData[0]?.providerId || "password", displayName: u.displayName || "" });
  const get = async (col, id) => { const s = await fb.getDoc(fb.doc(db, col, id)); return s.exists() ? s.data() : null; };
  const wait = new Promise(r => { const off = fb.onAuthStateChanged(auth, () => { off(); r(); }); });
  return {
    modo: "firebase",
    listo: wait,
    actual: () => U(auth.currentUser),
    onAuth: cb => fb.onAuthStateChanged(auth, u => cb(U(u))),
    async registrar(email, clave) {
      const c = await fb.createUserWithEmailAndPassword(auth, email, clave);
      try { await fb.sendEmailVerification(c.user); } catch {}
      return U(c.user);
    },
    async ingresar(email, clave) { return U((await fb.signInWithEmailAndPassword(auth, email, clave)).user); },
    async ingresarGoogle() { return U((await fb.signInWithPopup(auth, new fb.GoogleAuthProvider())).user); },
    salir: () => fb.signOut(auth),
    async recuperar(email) { await fb.sendPasswordResetEmail(auth, email); return {}; },
    async cambiarClave(actual, nueva) {
      const u = auth.currentUser; await fb.reauthenticateWithCredential(u, fb.EmailAuthProvider.credential(u.email, actual)); await fb.updatePassword(u, nueva);
    },
    async reenviarVerificacion() { await fb.sendEmailVerification(auth.currentUser); },
    async recargar() { await auth.currentUser.reload(); await auth.currentUser.getIdToken(true); return U(auth.currentUser); },
    cargarPerfil: uid => get("usuarios", uid),
    async guardarPerfil(uid, perfil, nuevo) {
      const b = fb.writeBatch(db);
      b.set(fb.doc(db, "usuarios", uid), { ...perfil, actualizado: fb.serverTimestamp() }, { merge: !nuevo });
      if (nuevo) b.set(fb.doc(db, "cedulas", perfil.cedula), { uid });
      try { await b.commit(); } catch (e) { if (nuevo && e.code === "permission-denied") { const err = new Error("cedula-duplicada"); throw err; } throw e; }
    },
    cargarProgreso: uid => get("progreso", uid),
    guardarProgreso: (uid, p) => fb.setDoc(fb.doc(db, "progreso", uid), { ...p, actualizado: fb.serverTimestamp() }),
    async cargarCalificaciones(uid) { return (await get("calificaciones", uid))?.oficial || {}; },
    async esDocente(u) { if (!u?.emailVerified) return false; try { return !!(await get("docentes", u.email)); } catch { return false; } },
    async listarAlumnos() {
      const [us, pr, ca] = await Promise.all(["usuarios", "progreso", "calificaciones"].map(c => fb.getDocs(fb.collection(db, c))));
      const m = {}; us.forEach(d => m[d.id] = { uid: d.id, perfil: d.data(), progreso: {}, oficial: {} });
      pr.forEach(d => m[d.id] && (m[d.id].progreso = d.data())); ca.forEach(d => m[d.id] && (m[d.id].oficial = d.data().oficial || {}));
      return Object.values(m);
    },
    guardarCalificaciones: (uid, oficial) => fb.setDoc(fb.doc(db, "calificaciones", uid), { oficial, actualizado: fb.serverTimestamp() }),
  };
}

/* ===================== DEMO (localStorage) ===================== */
async function hash(s) { const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, "0")).join(""); }
function crearDemo(cfg) {
  const K = "cvd_demo_db", KS = "cvd_demo_sesion";
  const rd = () => { try { return JSON.parse(localStorage.getItem(K)) || {}; } catch { return {}; } };
  const db0 = () => Object.assign({ cuentas: {}, usuarios: {}, progreso: {}, calificaciones: {}, cedulas: {} }, rd());
  const wr = d => { try { localStorage.setItem(K, JSON.stringify(d)); } catch {} };
  const listeners = [];
  const sesion = () => { try { return localStorage.getItem(KS); } catch { return null; } };
  const U = email => { const d = db0(), c = d.cuentas[email]; return c ? { uid: c.uid, email, emailVerified: true, proveedor: c.proveedor, displayName: c.displayName || "" } : null; };
  const emit = () => { const u = sesion() ? U(sesion()) : null; listeners.forEach(f => f(u)); };
  const err = code => Object.assign(new Error(code), { code });
  const uid = () => "demo_" + crypto.getRandomValues(new Uint32Array(2)).join("");
  const setSes = e => { try { e ? localStorage.setItem(KS, e) : localStorage.removeItem(KS); } catch {} emit(); };
  return {
    modo: "demo", listo: Promise.resolve(),
    actual: () => (sesion() ? U(sesion()) : null),
    onAuth: cb => { listeners.push(cb); setTimeout(() => cb(sesion() ? U(sesion()) : null)); },
    async registrar(email, clave) {
      email = email.toLowerCase(); const d = db0(); if (d.cuentas[email]) throw err("auth/email-already-in-use");
      const salt = uid(); d.cuentas[email] = { uid: uid(), salt, h: await hash(salt + clave), proveedor: "password" }; wr(d); setSes(email); return U(email);
    },
    async ingresar(email, clave) {
      email = email.toLowerCase(); const c = db0().cuentas[email];
      if (!c || c.proveedor !== "password" || c.h !== await hash(c.salt + clave)) throw err("auth/invalid-credential");
      setSes(email); return U(email);
    },
    async ingresarGoogle() {
      const e = (prompt("MODO DEMO — escribí un correo de Google simulado:") || "").trim().toLowerCase(); if (!e) throw err("auth/popup-closed-by-user");
      const d = db0(); if (!d.cuentas[e]) { d.cuentas[e] = { uid: uid(), proveedor: "google.com", displayName: e.split("@")[0] }; wr(d); } setSes(e); return U(e);
    },
    async salir() { setSes(null); },
    async recuperar(email) {
      email = email.toLowerCase(); const d = db0(), c = d.cuentas[email]; if (!c || c.proveedor !== "password") return {};
      const tmp = "Temp" + Math.floor(1000 + Math.random() * 9000) + "x"; c.h = await hash(c.salt + tmp); wr(d); return { demo: `MODO DEMO: en producción recibirías un correo con un enlace. Tu contraseña temporal es: ${tmp}` };
    },
    async cambiarClave(actual, nueva) {
      const e = sesion(), d = db0(), c = d.cuentas[e]; if (c.h !== await hash(c.salt + actual)) throw err("auth/invalid-credential"); c.h = await hash(c.salt + nueva); wr(d);
    },
    async reenviarVerificacion() {}, async recargar() { return U(sesion()); },
    async cargarPerfil(u) { return db0().usuarios[u] || null; },
    async guardarPerfil(u, perfil, nuevo) {
      const d = db0(); if (nuevo && d.cedulas[perfil.cedula] && d.cedulas[perfil.cedula] !== u) throw err("cedula-duplicada");
      d.usuarios[u] = { ...(d.usuarios[u] || {}), ...perfil }; if (nuevo) d.cedulas[perfil.cedula] = u; wr(d);
    },
    async cargarProgreso(u) { return db0().progreso[u] || null; },
    async guardarProgreso(u, p) { const d = db0(); d.progreso[u] = p; wr(d); },
    async cargarCalificaciones(u) { return db0().calificaciones[u] || {}; },
    async esDocente(u) { return !!u && (cfg.demo?.docentes || []).includes(u.email); },
    async listarAlumnos() { const d = db0(); return Object.entries(d.usuarios).map(([u, perfil]) => ({ uid: u, perfil, progreso: d.progreso[u] || {}, oficial: d.calificaciones[u] || {} })); },
    async guardarCalificaciones(u, o) { const d = db0(); d.calificaciones[u] = o; wr(d); },
  };
}

export async function crearBackend(cfg) {
  if (cfg.firebase?.apiKey) return crearFirebase(cfg);
  return crearDemo(cfg);
}
