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
# pd: Es un alias que se utiliza comúnmente para referirse a la biblioteca pandas.
# read_csv("BD_TABANTAJ.csv", encoding="ISO-8859-1"): Esta es una función de pandas que se utiliza para leer datos de un
# archivo CSV y cargarlos en un DataFrame. Aquí hay dos argumentos importantes:
# "BD_TABANTAJ.csv": Este es el nombre del archivo CSV que deseas leer. Debes asegurarte de que el archivo esté en el mismo
# directorio que tu script de Python o proporcionar la ruta completa si se encuentra en otro lugar.
# encoding="ISO-8859-1": Esto especifica el tipo de codificación utilizada en el archivo CSV. El valor "ISO-8859-1" se utiliza
# cuando el archivo contiene caracteres extendidos, como acentos y otros caracteres especiales. Es importante usar la codificación
# correcta para asegurarte de que los caracteres se lean correctamente.

# Obtener las opciones del filtro a partir de una columna del DataFrame
opciones_filtro = [{"label": "Todas las categorías", "value": "Todas"}] + [
    {"label": area, "value": area} for area in df["area"].unique()
]
# Esto inicializa la lista opciones_filtro con un primer elemento.         Esto es una comprensión de lista que recorre los valores únicos en la
# Este primer elemento representa la opción "Todas las categorías"        columna "area" del DataFrame df. Por cada valor único, crea un diccionario
# en el filtro. El valor label se mostrará en el filtro y el valor        con una etiqueta (label) que es el valor del área y un valor (value) que
# value se utilizará internamente en la aplicación para identificar       también es el valor del área. Básicamente, estamos creando una lista de
# esta opción.                                                            diccionarios donde cada diccionario representa una opción en el filtro de área
# +: El operador + se utiliza aquí para concatenar dos listas. En
# este caso, la primera lista contiene la opción "Todas las categorías",
# y la segunda lista se genera en el siguiente paso.


# Definir el diseño del dashboard
# Segmento 1
app.layout = html.Div(
    children=[
        # Este es un argumento dentro de la función html.Div() que espera una lista de componentes HTML que se incluirán en este Div.
        html.H1(
            # Aquí estás creando un encabezado de nivel 1 (<h1>) en HTML. Dentro del encabezado, estás insertando el texto "Dashboard tickets".
            # Esto será el título principal de tu dashboard.
            "Dashboard tickets",
            style={"textAlign": "center", "color": "#503D36", "font_size": 30},
            # style={"textAlign": "center", "color": "#503D36", "font_size": 30}: Esto define un diccionario de estilo que se aplica al elemento <h1>.
            # "textAlign": "center": Esto centra el texto del título en la página.
            # "color": "#503D36": Esto define el color del texto del título. El código de color #503D36 se refiere a un tono específico.
            # "font_size": 30: Esto establece el tamaño de la fuente del título en 30.
        ),
        # Segmento 2
        html.Div(
            # Esto crea un contenedor div en HTML. Los corchetes [...] son utilizados para especificar los elementos hijos que se encuentran dentro del div.
            [
                html.Div(
                    dcc.Dropdown(
                        # Aquí estás creando un div que contiene un componente Dropdown de Dash.
                        id="filtro",
                        # id="filtro": Esto asigna un ID único al Dropdown. Este ID se utilizará más adelante en el código para identificar y acceder
                        # a este componente
                        options=opciones_filtro,
                        # Aquí estás proporcionando las opciones para el menú desplegable. opciones_filtro es una lista de diccionarios que especifican
                        # las opciones y valores posibles para el filtro.
                        value="Todas",
                        # Esto establece el valor predeterminado seleccionado en el menú desplegable.
                    )
                )
            ],
        ),
        # Segmento 3
        html.Div(
            [
                html.Div(dcc.Graph(id="proyecto_plot")),
                html.Div(dcc.Graph(id="categoria_plot")),
            ],
            style={"display": "flex"},
        ),
        # style={"display": "flex"}): Esto crea un contenedor div en HTML y establece un estilo para él. El estilo "display": "flex"
        # se utiliza para aplicar el modelo de diseño flexible (Flexbox) en CSS, que permite organizar los componentes internos de manera flexible en
        # relación con el contenedor.
        # Segment 4
        html.Div(
            [
                html.Div(dcc.Graph(id="totales_plot")),
                html.Div(dcc.Graph(id="area_plot")),
            ],
            style={"display": "flex"},
        ),
    ]
)


# Definir la función de actualización de las gráficas
@app.callback(
    # Esto es una decoración que indica que la siguiente función se usará como una devolución de llamada. Las devoluciones
    # de llamada se activan en respuesta a eventos en tu aplicación, como cambios en los valores de entrada.
    Output("proyecto_plot", "figure"),
    # Output("proyecto_plot", "figure"): Esto indica que la salida de esta función de devolución de llamada afectará a la figura de la gráfica con el ID "proyecto_plot".
    Output("categoria_plot", "figure"),
    # Output("categoria_plot", "figure"): Similar al anterior, esto indica que la salida afectará a la figura de la gráfica con el ID "categoria_plot".
    Output("totales_plot", "figure"),
    # Output("totales_plot", "figure"): Esto indica que la salida afectará a la figura de la gráfica con el ID "totales_plot".
    Output("area_plot", "figure"),
    # Output("area_plot", "figure"): Esto indica que la salida afectará a la figura de la gráfica con el ID "area_plot".
    Input("filtro", "value"),
    ##Input("filtro", "value"): Esto establece que esta función de devolución de llamada se activará cuando el valor del componente con el ID "filtro"
    # cambie. En otras palabras, cuando el usuario seleccione una nueva opción en el menú desplegable de filtro.
)

# En resumen, esta función de devolución de llamada se ejecutará cuando el valor del filtro cambie. Su objetivo es actualizar las figuras de las gráficas "proyecto_plot",
#  "categoria_plot", "totales_plot" y "area_plot" en función del nuevo valor del filtro. La función tomará el nuevo valor del filtro como entrada y generará las figuras
# actualizadas para las gráficas correspondientes.


def actualizar_graficas(valor_filtro):
    # def actualizar_graficas(valor_filtro):: Esto define una función llamada actualizar_graficas que toma un argumento valor_filtro.
    # Esta función se utilizará como una devolución de llamada para actualizar las gráficas en respuesta a cambios en el filtro.
    if valor_filtro == "Todas":
        # if valor_filtro == "Todas":: Esto verifica si el valor seleccionado en el filtro es igual a la cadena "Todas". En caso de ser
        # cierto (cuando se selecciona "Todas" en el filtro), se ejecutará el bloque de código que sigue.
        datos_filtrados = df
    # datos_filtrados = df: Cuando se selecciona "Todas" en el filtro, esta línea simplemente asigna todo el DataFrame df a la variable datos_filtrados.
    # En otras palabras, no se realiza ningún filtrado, y todas las filas del DataFrame original se mantienen en datos_filtrados.
    else:
        # Esto marca el comienzo del bloque de código que se ejecutará si la condición del if no se cumple, es decir, cuando no se selecciona "Todas"
        # en el filtro.
        datos_filtrados = df[df["area"] == valor_filtro]
    # datos_filtrados = df[df["area"] == valor_filtro]: En este caso, se utiliza una indexación booleana para filtrar el DataFrame df en función del valor
    # seleccionado en el filtro. La parte df["area"] == valor_filtro crea una Serie booleana que es True para las filas donde la columna "area"
    # coincide con valor_filtro y False para las demás filas. Luego, se utiliza esta Serie booleana para filtrar df, de modo que datos_filtrados
    # contendrá solo las filas donde la columna "area" coincide con valor_filtro.

    # En este fragmento de código, se esta definiendo una función actualizar_graficas que se activa cada vez que se cambia el valor del filtro. Si bien esto no es
    # una API en el sentido tradicional de comunicarse con un servidor externo, sigue el concepto de una API en el sentido de que estás proporcionando una
    # interfaz (la función actualizar_graficas) a través de la cual puedes obtener datos y resultados (las figuras de las gráficas) basados en una entrada
    # específica (el valor del filtro

    # Visualizaciones de tipo "GRAFICAS DE COLUMNAS AGRUPADAS"

    # Tickets por proyecto
    proyecto_plot = go.Figure()
    # Aquí estás creando una nueva figura utilizando go.Figure() de Plotly. Una
    # figura en Plotly es un contenedor para todas tus visualizaciones.
    # Esto marca el comienzo de la construcción de tu gráfica.

    for label_value in df["LABEL"].unique():
        # Este bucle for itera a través de los valores únicos en la columna "LABEL" del DataFrame df.
        # Por cada valor único, se creará una visualización de barra en la gráfica.
        datos_label = datos_filtrados[datos_filtrados["LABEL"] == label_value]
        # Aquí, datos_label es un nuevo DataFrame que contiene solo las filas de datos_filtrados donde
        # la columna "LABEL" coincide con el valor actual en la iteración del bucle. Esto está filtrando
        # tus datos para el valor de "LABEL" actual.
        proyecto_suma = datos_label.groupby("Fecha_de_creacion")["count-area"].sum()
        # Esto agrupa los datos en datos_label por la columna "Fecha_de_creacion" y luego suma la columna
        # "count-area" para cada grupo. Esto se hace para crear la suma total de "count-area" por fecha.
        # La variable proyecto_suma contendrá los valores de suma calculados.
        proyecto_plot.add_trace(
            go.Bar(x=proyecto_suma.index, y=proyecto_suma.values, name=label_value)
        )
    # Aquí, estás añadiendo una nueva traza a la figura proyecto_plot. Una traza es una visualización
    # individual en una figura. Estás usando go.Bar para crear una visualización de barras. Los argumentos
    # x y y indican las posiciones en el eje x (las fechas) y las alturas de las barras (los valores de suma),
    # respectivamente. El argumento name define la etiqueta de la leyenda de esta traza, que será el valor
    # actual en la iteración del bucle (valor único en la columna "LABEL").
    proyecto_plot.update_layout(
        title="Tickets por proyecto", xaxis_title="Fecha", yaxis_title=""
    )
    #    #En Plotly, update_layout es un método que te permite modificar y personalizar varios aspectos del diseño de tu gráfica.
    # En este caso, estás utilizando update_layout para personalizar los títulos de los ejes x e y de la visualización area_plot.

    # Cantidad de tickets por area
    area_suma = datos_filtrados.groupby("area")["count-area"].sum()
    # Aquí estás agrupando los datos en datos_filtrados por la columna "area" y luego sumando los valores de la columna "count-area"
    # para cada grupo. Esto significa que estás calculando la suma total de "count-area" para cada valor único en la columna "area".
    # La variable area_suma contendrá estos valores de suma y los índices del DataFrame serán los valores únicos en la columna "area".

    area_plot = px.bar(
        x=area_suma.values,
        # Los valores en el eje x (horizontal) de la visualización serán las sumas de "count-area" que calculaste previamente. Estas sumas
        # se encuentran en area_suma.values.
        y=area_suma.index,
        # Los valores en el eje y (vertical) de la visualización serán los valores únicos en la columna "area". Estos valores se encuentran
        # en el índice de area_suma.
        title="Cantidad de tickets por área",
        orientation="h",
    )
    area_plot.update_layout(xaxis_title="Área", yaxis_title="")

    # Visualizaciones de tipo "GRAFICO DE AREAS"

    # Cantidad de tickets totales
    totales_por_fecha = datos_filtrados.groupby("Fecha_de_creacion")[
        "Fecha_de_creacion"
    ].count()
    # .groupby("Fecha_de_creacion"): Esto realiza una operación de agrupamiento por la columna "Fecha_de_creacion". En otras palabras,
    # estás agrupando tus datos por fechas.Fecha_de_creacion"]: Aquí estás seleccionando la columna "Fecha_de_creacion" del DataFrame
    # después del agrupamiento. Esto se hace para poder realizar operaciones en esa columna específica.
    # .count(): Esto calcula el recuento de ocurrencias de cada fecha en la columna "Fecha_de_creacion" después del agrupamiento.
    # En otras palabras, estás contando cuántas veces aparece cada fecha en tus datos.
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
    # datos_filtrados["CATEGORIA"]: Esto selecciona la columna "CATEGORIA" del DataFrame datos_filtrados. Esto crea una Serie de pandas que contiene los valores
    # en la columna "CATEGORIA".
    # .value_counts(): Esto es un método de pandas que se aplica a una Serie. En este caso, se utiliza para contar las ocurrencias de cada valor en la Serie.
    # Para cada valor único en la columna "CATEGORIA", este método devuelve el número de veces que aparece en la columna.

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
