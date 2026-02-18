import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Performance Realizada", layout="wide")
st.title("📊 Performance de Custos (Realizado)")

try:
    # Timeout de 5 segundos para não travar a tela
    res = requests.get("http://api:8000/metrics/comparison", timeout=5)
    
    if res.status_code == 200:
        data = res.json()
        realizado_dict = data.get("realizado", {})

        if realizado_dict:
            df_real = pd.DataFrame(list(realizado_dict.items()), columns=['Categoria', 'Valor'])
            
            # KPI Card
            total_realizado = df_real['Valor'].sum()
            st.metric("Total Realizado Acumulado", f"R$ {total_realizado:,.2f}")
            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                fig_pie = px.pie(df_real, values='Valor', names='Categoria', hole=0.4, title="Mix de Gastos")
                st.plotly_chart(fig_pie, use_container_width=True)
            with col2:
                fig_bar = px.bar(df_real.sort_values(by="Valor"), x='Valor', y='Categoria', orientation='h', title="Ranking")
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("💡 API conectada, mas a tabela 'financial_records' está vazia.")
    else:
        st.error(f"❌ A API retornou erro {res.status_code}: {res.text}")

except Exception as e:
    st.error(f"❌ Erro de Conexão: A API em http://api:8000 não respondeu. Verifique se o container 'api' está em UP.")