import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Performance de Custos", layout="wide")
st.title("📊 Performance de Custos e P&L")

# Tentativa de conexão
try:
    # Use 'api' se estiver dentro do Docker ou 'localhost' se rodando local
    url = "http://api:8000/metrics/comparison" 
    res = requests.get(url, timeout=5)
    
    if res.status_code == 200:
        data = res.json()
        realizado = data.get("realizado", {})
        orcado = data.get("orcado", {})

        if realizado or orcado:
            categorias = list(set(list(realizado.keys()) + list(orcado.keys())))
            df_plot = pd.DataFrame([
                {
                    "Categoria": cat, 
                    "Realizado": realizado.get(cat, 0), 
                    "Orçado": orcado.get(cat, 0)
                } for cat in categorias
            ])

            # Gráfico de Barras
            st.subheader("Comparativo Realizado vs Orçado")
            fig = px.bar(df_plot, x="Categoria", y=["Orçado", "Realizado"], barmode="group")
            st.plotly_chart(fig, use_container_width=True)
            
            st.table(df_plot)
        else:
            st.warning("⚠️ Banco de dados conectado, mas as tabelas estão vazias.")
    else:
        st.error(f"❌ Erro na API: Status {res.status_code}")

except Exception as e:
    st.error(f"⚠️ Falha total de conexão com a API: {e}")