import streamlit as st
import requests

st.set_page_config(page_title="Cadastrar Budget", layout="wide")

st.title("📑 Planejamento de Budget (Tabela: budget_records)")

with st.form("form_budget_records", clear_on_submit=True):
    st.subheader("Configurações do Orçamento")
    month = st.text_input("Mês de Referência (Ex: jul/25)", value="jul/25")
    
    col1, col2 = st.columns(2)
    with col1:
        salarios = st.number_input("Salários", min_value=0.0, format="%.2f")
        beneficios = st.number_input("Benefícios", min_value=0.0, format="%.2f")
        va_vr = st.number_input("VA / VR", min_value=0.0, format="%.2f")
    
    with col2:
        saude = st.number_input("Plano de Saúde", min_value=0.0, format="%.2f")
        encargos = st.number_input("Encargos", min_value=0.0, format="%.2f")
        bonus = st.number_input("Bônus", min_value=0.0, format="%.2f")

    submit = st.form_submit_button("💾 Registrar no Orçado")

    if submit:
        # Montando o payload exatamente para a tabela budget_records
        payload = [
            {"category": "Salários", "value": salarios, "month_ref": month},
            {"category": "Benefícios", "value": beneficios, "month_ref": month},
            {"category": "VA / VR", "value": va_vr, "month_ref": month},
            {"category": "Plano de Saúde", "value": saude, "month_ref": month},
            {"category": "Encargos", "value": encargos, "month_ref": month},
            {"category": "Bônus", "value": bonus, "month_ref": month}
        ]
        
        try:
            # Rota /budget do seu main.py (conforme definido na sua última versão da API)
            response = requests.post("http://api:8000/budget", json=payload)
            
            if response.status_code == 200:
                st.success(f"✅ Budget de {month} salvo com sucesso em budget_records!")
            else:
                st.error(f"❌ Erro na API: {response.text}")
        except Exception as e:
            st.error(f"⚠️ Falha de conexão: {e}")