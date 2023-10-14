import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)


# read csv from a URL
@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_excel("Consulta_Cassio.xlsm", engine="openpyxl")

df = get_data()

# dashboard title
st.title("Consulta de ISOL")

# top-level filters
job_filter = st.multiselect("Selecione o(s) ISOL(s)", pd.unique(df["ISOL PARADA"]), max_selections = 3, placeholder = 'Escolha um ISOL')

number_of_columns = len(job_filter)

print(job_filter)

def function_page(i: int, job_filter: list, df: pd.DataFrame):

    df = df[df["ISOL PARADA"] == job_filter[i]].reset_index(drop=True)
    df = df[["LT","KKS","STATUS","DESCRIÇÃO ATIVIDADE"]]

    # Group the data according to the columns categories 
    def sort_function(v):
        if (v=='AG.LIBERAÇÃO'):
            return 1
        elif (v=='APR.PLN.MN'):
            return 2
        elif (v=='LIB.P/EXECUÇÃO'):
            return 3
        elif (v=='TAREFA INICIADA'):
            return 4
        elif (v=='CANCELADA'):
            return 5
        elif (v=='AG.LIB.P/TESTE'):
            return 6
        elif (v=='LIB.P/TESTE'):
            return 7
        elif (v=='TRF.ENCERRADA'):
            return 8
        elif (v=='LIB.P/ARQUIVAR'):
            return 9 
        elif (v=='ARQUIVADA'):
            return 10
    df['aux'] = df['STATUS'].apply(sort_function)
    df = df.sort_values(by = 'aux')
    df = df.drop('aux', axis = 1)
    pd.set_option('colheader_justify', 'center')
    # Highlight cells
    def style_cases(v):
        if (v=='AG.LIBERAÇÃO'):
            return 'background-color:white; font-weight: bold; color:black;'
        elif (v=='APR.PLN.MN'):
            return 'background-color:purple; font-weight: bold; color:black;'
        elif (v=='LIB.P/EXECUÇÃO'):
            return 'background-color:green; font-weight: bold; color:black;'
        elif (v=='TAREFA INICIADA'):
            return 'background-color:yellow; font-weight: bold; color:black;'
        elif (v=='CANCELADA'):
            return 'background-color:gray; font-weight: bold; color:black;'
        elif (v=='AG.LIB.P/TESTE'):
            return 'background-color:white; font-weight: bold; border-style: solid; border-color: blue;' 
        elif (v=='LIB.P/TESTE'):
            return 'background-color:blue; font-weight: bold; color:black;' 
        elif (v=='TRF.ENCERRADA'):
            return 'background-color:red; font-weight: bold; color:black;' 
        elif (v=='LIB.P/ARQUIVAR') or (v=='ARQUIVADA'):
            return 'background-color:black; font-weight: bold; color:white;' 

        
    sdf = df.style.applymap(style_cases, subset = 'STATUS')

    fmt_dict = {'AG.LIBERAÇÃO':'background-color:white; font-weight: bold; color:black;',
                'APR.PLN.MN':'background-color:purple; font-weight: bold; color:black;',
                'LIB.P/EXECUÇÃO':'background-color:green; font-weight: bold; color:black;',
                'TAREFA INICIADA':'background-color:yellow; font-weight: bold; color:black;',
                'CANCELADA':'background-color:gray; font-weight: bold; color:black;',
                'AG.LIB.P/TESTE':'background-color:white; font-weight: bold; color:black; border-style: solid; border-color: blue; border-width: 40px;',
                'LIB.P/TESTE':'background-color:blue; font-weight: bold; color:black;',
                'TRF.ENCERRADA':'background-color:red; font-weight: bold; color:black;',
                'LIB.P/ARQUIVAR':'background-color:black; font-weight: bold; color:white;',
                'ARQUIVADA':'background-color:black; font-weight: bold; color:white;',
                'PENDENTE':'background-color:white; font-weight: bold; color:black;'}

    def fmt(data, fmt_dict):
        return data.replace(fmt_dict)

    # Highlight cells
    sdf = df.style.apply(fmt, fmt_dict=fmt_dict, subset=['STATUS'])

    st.markdown("<h1 style='text-align: left;'>LT's da ISOL {}</h1>".format(job_filter[i]), unsafe_allow_html=True)

    

    return sdf

    
    
if number_of_columns != 0:
    cols = [0]*number_of_columns
    cols = st.columns(number_of_columns)
    for i in range(len(cols)):
        with cols[i]:
            sdf = function_page(i, job_filter, df)
            st.data_editor(sdf,
                disabled=True,
                column_config={
                        "LT": st.column_config.NumberColumn("LT", help="Número da LT", min_value=0, max_value=10000000, step=1, format="%d"),
                        "DESCRIÇÃO ATIVIDADE": st.column_config.Column("DESCRIÇÃO DA ATIVIDADE", help = "Descrição da atividade", width='None')
                    },                
                hide_index=True,
                use_container_width=False,
                width = 600,
                height = 300
            )
            