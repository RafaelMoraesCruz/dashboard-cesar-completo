import streamlit as st
import pandas as pd
from PIL import Image

df = pd.read_excel("./data/acidentes2021.xlsx")
back_img = Image.open('./data/img/transito-recife.jpg')

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


with header:
    st.title("ESTUDO DE ACIDENTES NA CIDADE DO RECIFE")
    st.image(back_img)
    st.text("Este primeiro app tem como exemplo testar inputs e basic funtions")
