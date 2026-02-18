import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Comparativo", layout="wide")
st.title("⚖️ Realizado vs Orçado")

try:
    res = requests.get("http://api:8000/metrics/comparison", timeout=5)
    data = res.json()
    
    realizado = data.get("realizado", {})
    orcado = data.get("orcado", {})

    if realizado or orcado:
        todas_cats = list(set(list(realizado.keys()) + list(orcado.keys())))
        lista_comp = []
        for cat in todas_cats:
            lista_comp.append({
                "Categoria": cat,
                "Realizado": realizado.get(cat, 0),
                "Orçado": orcado.get(cat, 0)
            })
        
        df = pd.DataFrame(lista_comp)
        st.dataframe(df, use_container_width=True)
        # Se quiser gráfico, adicione um st.bar_chart(df.set_index('Categoria')) aqui
    else:
        st.info("💡 Cadastre dados em 'ingestao' e 'cadastrar budget' para comparar.")

except Exception:
    st.error("❌ Falha na comunicação com o banco de dados.")