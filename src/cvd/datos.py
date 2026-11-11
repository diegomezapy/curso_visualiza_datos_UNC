"""Carga de datasets del curso. Todos son sintéticos y reproducibles (ver datos/README.md)."""
import pandas as pd
from .estilo import raiz_proyecto

def _csv(nombre, **kw):
    return pd.read_csv(raiz_proyecto() / "datos" / nombre, **kw)

def ventas():       return _csv("ventas_retail.csv", parse_dates=["fecha"])
def notas():        return _csv("notas_estudiantes.csv")
def departamentos():return _csv("departamentos_py.csv")
def anscombe():     return _csv("anscombe.csv")
def serie_diaria(): return _csv("demanda_energia.csv", parse_dates=["fecha"])
