import streamlit as st
import pandas as pd
import requests

st.title(" Ingestão de Dados")

API_URL = "http://api:8000/subscribe"

tab1, tab2 = st.tabs(["📄 Upload de Arquivo", "📝 Entrada Manual"])

with tab1:
    arquivo = st.file_uploader("Suba seu CSV ou Excel", type=['csv', 'xlsx'])
    if arquivo:
        df = pd.read_csv(arquivo) if arquivo.name.endswith('.csv') else pd.read_excel(arquivo)
        st.dataframe(df.head())
        
        if st.button("Enviar para o Banco"):
            for _, row in df.iterrows():
                payload = {"customer_name": str(row['customer_name']), "mrr_value": float(row['mrr_value'])}
                requests.post(API_URL, json=payload)
            st.success("Dados enviados com sucesso!")

with tab2:
    with st.form("manual"):
        nome = st.text_input("Nome do Cliente")
        valor = st.number_input("Valor MRR", min_value=0.0)
        if st.form_submit_button("Salvar"):
            payload = {"customer_name": nome, "mrr_value": valor}
            res = requests.post(API_URL, json=payload)
            if res.status_code == 200:
                st.success("Venda registrada!")