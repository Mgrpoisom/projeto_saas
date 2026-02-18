import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="KPIs Financeiros", layout="wide")

st.title("📈 Performance de Receita (MRR)")

try:
    # Consome os dados que você enviou
    res = requests.get("http://api:8000/metrics/mrr")
    data = res.json()

    # Exibição de Cards de Destaque
    col1, col2, col3 = st.columns(3)
    col1.metric("MRR Total", f"R$ {data['total_mrr']:,.2f}")
    col2.metric("Clientes Ativos", data['active_customers'])
    col3.metric("Ticket Médio", f"R$ {(data['total_mrr']/data['active_customers']):,.2f}")

    # Criando o DataFrame para o gráfico
    df_visual = pd.DataFrame({
        "Métrica": ["MRR Atual", "Meta Mensal"],
        "Valor": [data['total_mrr'], 10000000.00] # Meta de 10M como exemplo
    })

    # Gráfico de Barras Profissional
    fig = px.bar(
        df_visual, 
        x="Métrica", 
        y="Valor", 
        color="Métrica",
        text_auto='.3s',
        title="Progresso em relação à Meta",
        color_discrete_map={"MRR Atual": "#00CC96", "Meta Mensal": "#636EFA"}
    )
    
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao conectar com a API: {e}")