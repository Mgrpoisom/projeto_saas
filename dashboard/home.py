import streamlit as st
import requests

st.set_page_config(page_title="Projeto Zero - Home", layout="wide")

st.title(" Bem-vindo ao Projeto Zero")

# Tenta conectar na API usando o nome do serviço 'api'
try:
    response = requests.get("http://api:8000/")
    if response.status_code == 200:
        st.success("Backend conectado com sucesso!")
        
        # Busca métricas reais da API
        metrics = requests.get("http://api:8000/metrics/mrr").json()
        col1, col2 = st.columns(2)
        col1.metric("MRR Total", f"R$ {metrics['total_mrr']:.2f}")
        col2.metric("Clientes Ativos", metrics['active_customers'])
    else:
        st.warning(" API online, mas retornou um erro.")
except Exception as e:
    st.error(" Erro ao conectar na API. Verifique se o container 'api' está rodando.")

st.info("Utilize o menu lateral para acessar a página de Ingestão de Dados.")