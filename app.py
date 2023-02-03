from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from utils import DATA_PATH, create_lista_bairros


df = pd.read_excel(DATA_PATH)
lista_bairros = create_lista_bairros(df)


app = Dash(__name__)


app.layout = html.Div(
    [
        html.H1("Dashboard CESAR School grupo 5"),
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Digite o Bairro para análise:"),
                        dcc.Dropdown(
                            options=lista_bairros, value="TODOS", id="dropdown_bairros"
                        ),
                        html.H4("Selecione o tipo:"),
                        dcc.Dropdown(
                            options=[
                                "natureza_acidente",
                                "ciclom",
                                "auto",
                                "vitimas",
                                "tempo_clima",
                                "sinalizacao",
                            ],
                            value="vitimas",
                            id="dropdown_legenda",
                        ),
                    ],
                    className="dropdowns-div",
                ),
                html.Div([dcc.Graph(id="figura1")]),
                html.Div([dcc.Graph(id="figura2")]),
            ],
            className="div-1st-graph",
        ),
    ],
    className="major-div",
)


@app.callback(
    Output("figura1", "figure"),
    Output("figura2", "figure"),
    Input("dropdown_bairros", "value"),
    Input("dropdown_legenda", "value"),
)
def update_output(bairro, legenda):
    if bairro == "TODOS" or bairro == None:
        bairro = "TODOS"
        df4 = df.copy()
        df4["hora"] = df4["hora"].apply(lambda x: x[0:2]).astype("int")
        df4_acidentes_hora = df4[(df4["hora"] >= 0) & (df4["hora"] <= 24)]

        fig = px.histogram(
            df4_acidentes_hora,
            x="hora",
            color=legenda,
            hover_data=df.columns,
            width=800,
            height=600,
        )
        fig.update_layout(
            title=f"<b>Distribuição da quantidade de acidentes por hora em {bairro} os bairros de Recife</b>",
            font=dict(size=10),
            yaxis_title="Quantidade de acidentes",
            xaxis_title="Hora do dia",
        )

        figpie = px.pie(
            df4,
            values=df4["natureza_acidente"].value_counts(normalize=True).values * 100,
            names=df4["natureza_acidente"].value_counts().index,
        )
        figpie.update_traces(
            hoverinfo="label",
            textinfo="percent",
            title=f"<b>Tipos de vítimas por acidentes em {bairro} os bairros</b>",
        )

        return fig, figpie
    else:
        df4 = df[df["bairro"] == bairro]
        df4["hora"] = df4["hora"].apply(lambda x: x[0:2]).astype("int")
        df4_acidentes_hora = df4[(df4["hora"] >= 0) & (df4["hora"] <= 24)]

        fig = px.histogram(
            df4_acidentes_hora,
            x="hora",
            color=legenda,
            hover_data=df.columns,
            width=800,
            height=600,
        )
        fig.update_layout(
            font=dict(size=10),
            title=f"<b>Distribuição da quantidade de acidentes por hora no bairro {bairro} de recife</b>",
            yaxis_title="Quantidade de acidentes",
            xaxis_title="Hora do dia",
        )

        figpie = px.pie(
            df4,
            values=df4["natureza_acidente"].value_counts(normalize=True).values * 100,
            names=df4["natureza_acidente"].value_counts().index,
        )
        figpie.update_traces(
            hoverinfo="label",
            textinfo="percent",
            title=f"<b>Tipos de vítimas por acidentes no bairro {bairro}</b>",
        )

        return fig, figpie


if __name__ == "__main__":
    app.run_server(debug=True)
