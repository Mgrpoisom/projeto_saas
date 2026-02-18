import streamlit as st
import requests

st.title("📥 Ingestão Manual - Projeto Zero")

# Criamos um formulário organizado para os dados de P&L
with st.form("manual_entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        area = st.selectbox("Área", ["Operações", "TI", "RH", "Vendas", "Marketing"]) #
        pl_line = st.text_input("Linha P&L (Ex: OPEX)") #
        category = st.text_input("Categoria (Ex: Software)") #
        provider = st.text_input("Fornecedor (Ex: Databricks)") #

    with col2:
        cost_center = st.text_input("Centro de Custo (Ex: 120202)") #
        value = st.number_input("Valor (R$)", min_value=0.0, format="%.2f") #
        month_ref = st.text_input("Mês de Referência (Ex: jul/26)") #

    submit_button = st.form_submit_button("Registrar no Banco de Dados")

    if submit_button:
        # Montamos o payload no formato de lista (bulk) que a API espera
        payload = [{
            "area": area,
            "pl_line": pl_line,
            "category": category,
            "cost_center": cost_center,
            "provider": provider,
            "value": value,
            "month_ref": month_ref
        }]
        
        try:
            # Enviamos para o endpoint /ingest que criamos
            response = requests.post("http://api:8000/ingest", json=payload)
            
            if response.status_code == 200:
                st.success(f"✅ Registro de {provider} salvo com sucesso!")
            else:
                st.error(f"❌ Erro na API: {response.json().get('detail')}")
        except Exception as e:
            st.error(f"⚠️ Erro de conexão: {e}")