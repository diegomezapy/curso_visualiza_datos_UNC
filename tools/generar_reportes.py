"""Genera los informes HTML por sucursal (ejecuta el lab 6 de punta a punta).
Programable con cron o GitHub Actions:  python tools/generar_reportes.py
"""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[1] / "sesiones/06_reporting_automatizado/lab06_reportes_automaticos.py"))
