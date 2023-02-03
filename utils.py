DATA_PATH = "./data/acidentes2021.xlsx"


def create_lista_bairros(df):
    list_bairros = []
    list_bairros.append('TODOS')
    for bairro in df['bairro'].unique():
        list_bairros.append(bairro)
    return list_bairros