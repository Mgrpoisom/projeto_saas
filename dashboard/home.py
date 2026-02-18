import streamlit as st
import requests

st.set_page_config(page_title="Projeto Zero", layout="wide")

st.title(" Bem-vindo ao Projeto Zero")

# Teste de conexão com a API
try:
    # 'api' é o nome do serviço no seu docker-compose
    check = requests.get("http://api:8000/")
    if check.status_code == 200:
        st.success(" Backend conectado com sucesso!")
    else:
        st.warning(" Backend respondeu, mas com erro.")
except:
    st.error("Não foi possível conectar ao Backend (API).")

st.info("Navegue pelo menu lateral para inserir novos dados via CSV ou Formulário.")