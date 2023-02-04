import streamlit as st
import pandas as pd
from PIL import Image
from utils import create_lista_bairros
import plotly.express as px
import numpy as np


df = pd.read_excel("./data/acidentes2021.xlsx")
back_img = Image.open('./data/img/transito-recife.jpg')
TAMANHO_DATASET = df.shape[0]

# filtros
lista_bairros = df["bairro"].unique()
lista_filtros = [
    "natureza_acidente",
    "ciclom",
    "auto",
    "vitimas",
    "tempo_clima",
    "sinalizacao",
]

st.set_page_config(
    page_title="DASHBOARD CESAR",
)

#ESTRUTURA
header = st.container()
dataset = st.container()
features = st.container()
grafico1 = st.container()


with header:
    st.title("ESTUDO DE ACIDENTES NA CIDADE DO RECIFE")
    st.image('http://transito.gtrans.com.br/cttupe/index.php/portal/getImg/192.168.10.120/')
    # st.image(back_img)

with dataset:
    st.title('Visualização incial do dataset')
    quantidade_itens = st.slider('Quantos itens deseja mostrar?', 0,TAMANHO_DATASET,(0,5))
    st.dataframe(df.iloc[quantidade_itens[0]:quantidade_itens[1],:])
    
with features:
    bairro = st.selectbox(
    'Selecione o bairro',
    options=create_lista_bairros(df))
    legenda = st.selectbox(
    'Selecione o filtro',
    options=lista_filtros)
    
with grafico1:
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
            values=df4[legenda].value_counts(normalize=True).values * 100,
            names=df4[legenda].value_counts().index,
        )
        figpie.update_traces(
            hoverinfo="label",
            textinfo="percent",
            title=f"<b>Tipos de {legenda} por acidentes em {bairro} os bairros</b>",
        )
        
        
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(figpie, use_container_width=True)
    
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
            values=df4[legenda].value_counts(normalize=True).values * 100,
            names=df4[legenda].value_counts().index,
        )
        figpie.update_traces(
            hoverinfo="label",
            textinfo="percent",
            title=f"<b>Tipos de {legenda} por acidentes no bairro {bairro}</b>",
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(figpie, use_container_width=True)