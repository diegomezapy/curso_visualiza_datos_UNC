/* Cada ejecución ocurre en un worker. El aula puede terminarlo si hay un bucle. */
let motor;
let cargando;
async function obtenerMotor() {
  if (!cargando) cargando = import("https://cdn.jsdelivr.net/pyodide/v314.0.8/full/pyodide.mjs")
    .then(({ loadPyodide }) => loadPyodide());
  motor = await cargando;
  return motor;
}

self.onmessage = async ({ data }) => {
  const { id, codigo, csv, grafico } = data;
  let globales;
  try {
    const py = await obtenerMotor();
    if (csv != null) py.FS.writeFile("datos.csv", csv, { encoding: "utf8" });
    if (grafico) await py.loadPackage("matplotlib");
    await py.loadPackagesFromImports(codigo);
    const salida = [];
    py.setStdout({ batched: linea => salida.push(linea) });
    py.setStderr({ batched: linea => salida.push(linea) });
    globales = py.globals.get("dict")();
    await py.runPythonAsync(codigo, { globals: globales });
    if (!globales.has("respuesta")) throw new Error("Creá la variable respuesta para comprobar el reto.");
    const objeto = globales.get("respuesta");
    const respuesta = objeto && typeof objeto.toJs === "function" ? objeto.toJs() : objeto;
    if (objeto && typeof objeto.destroy === "function") objeto.destroy();
    let imagen = null;
    if (grafico) {
      imagen = await py.runPythonAsync(`import matplotlib.pyplot as plt\nimport io, base64\nfiguras = plt.get_fignums()\n_codigo_png = None\nif figuras:\n    bufer = io.BytesIO()\n    plt.figure(figuras[-1]).savefig(bufer, format="png", bbox_inches="tight")\n    plt.close("all")\n    _codigo_png = base64.b64encode(bufer.getvalue()).decode("ascii")\n_codigo_png`, { globals: globales });
    }
    self.postMessage({ id, respuesta, imagen, salida: salida.slice(0, 30).join("\n") });
  } catch (error) {
    self.postMessage({ id, error: String(error?.message || error).slice(0, 1200) });
  } finally {
    globales?.destroy?.();
  }
};
