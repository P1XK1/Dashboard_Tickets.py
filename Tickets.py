import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Crear una aplicación Dash
app = dash.Dash(__name__)

# Cargar los datos (reemplaza 'datos.csv' con tu propio archivo)
df = pd.read_csv("BD_TABANTAJ.csv", encoding="ISO-8859-1")

# Obtener las opciones del filtro a partir de una columna del DataFrame
opciones_filtro = [{"label": "Todas las categorías", "value": "Todas"}] + [
    {"label": area, "value": area} for area in df["area"].unique()
]

# Definir el diseño del dashboard
app.layout = html.Div(
    children=[
        html.H1(
            "Dashboard tickets",
            style={"textAlign": "center", "color": "#503D36", "font_size": 30},
        ),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="filtro",
                        options=opciones_filtro,
                        value="Todas",
                        style={
                            "background-color": "white",
                            "border-color": "#F2F2F2",
                            "border-radius": "15px",
                            "border-width": "8px",
                            "color": "black",
                            "font_size": 30,
                        },
                    )
                )
            ],
        ),
        # Segment 2
        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        id="proyecto_plot",
                        className="create_container2 five columns",
                    )
                ),
                html.Div(
                    dcc.Graph(
                        id="categoria_plot",
                        className="create_container2 five columns",
                    )
                ),
            ],
        ),
        # Segment 3
        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        id="totales_plot",
                        className="create_container2 five columns",
                    )
                ),
                html.Div(
                    dcc.Graph(
                        id="area_plot",
                        className="create_container2 five columns",
                    )
                ),
            ],
        ),
    ]
)


# Definir la función de actualización de las gráficas
@app.callback(
    Output("proyecto_plot", "figure"),
    Output("categoria_plot", "figure"),
    Output("totales_plot", "figure"),
    Output("area_plot", "figure"),
    Input("filtro", "value"),
)
def actualizar_graficas(valor_filtro):
    if valor_filtro == "Todas":
        datos_filtrados = df
    else:
        datos_filtrados = df[df["area"] == valor_filtro]

    # Visualizaciones de tipo "GRAFICAS DE COLUMNAS AGRUPADAS"

    # Tickets por proyecto
    proyecto_plot = go.Figure()

    for label_value in df["LABEL"].unique():
        datos_label = datos_filtrados[datos_filtrados["LABEL"] == label_value]
        proyecto_suma = datos_label.groupby("Fecha_de_creacion")[
            "count-area"
        ].sum()  # Sumar "count-area" por fecha
        proyecto_plot.add_trace(
            go.Bar(
                x=proyecto_suma.index,
                y=proyecto_suma.values,
                name=label_value,
            )
        )

    proyecto_plot.update_layout(
        title="Tickets por proyecto", xaxis_title="Fecha", yaxis_title=""
    )

    # Cantidad de tickets por area
    area_suma = datos_filtrados.groupby("area")["count-area"].sum()

    area_plot = px.bar(
        x=area_suma.values,
        y=area_suma.index,
        title="Cantidad de tickets por área",
        orientation="h",
    )
    area_plot.update_layout(xaxis_title="Área", yaxis_title="")

    # Visualizaciones de tipo "GRAFICO DE AREAS"

    # Cantidad de tickets totales
    totales_por_fecha = datos_filtrados.groupby("Fecha_de_creacion")[
        "Fecha_de_creacion"
    ].count()
    totales_plot = px.area(
        totales_por_fecha,
        x=totales_por_fecha.index,
        y=totales_por_fecha.values,
        title="Cantidad de Tickets Totales",
    )
    totales_plot.update_layout(xaxis_title="Fecha", yaxis_title="Recuento")

    # Visualizaciones de tipo "GRAFICO DE BARRAS AGRUPADAS"

    # Tickets por categoria
    categoria_count = datos_filtrados["CATEGORIA"].value_counts()

    categoria_plot = px.bar(
        x=categoria_count.index,
        y=categoria_count.values,
    )
    categoria_plot.update_layout(
        title="Tickets por Categoria", xaxis_title="Cantidad", yaxis_title=""
    )

    return proyecto_plot, area_plot, totales_plot, categoria_plot


# Iniciar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
