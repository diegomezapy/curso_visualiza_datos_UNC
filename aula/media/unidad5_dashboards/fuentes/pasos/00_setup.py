import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
pio.templates.default = "plotly_white"

cubo = pd.read_csv("cubo_importaciones.csv")
cubo["fecha"] = pd.to_datetime(
    dict(year=cubo.anio, month=cubo.mes, day=1))
cubo["fob_mm"] = cubo.fob_usd / 1e6   # millones de USD
# La base no trae junio de 2025: se excluye ese mes
# de ambos años para comparar períodos iguales
cubo = cubo[cubo.mes != 6]
