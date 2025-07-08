import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Florio Dashboard", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .block-container { padding-top: 2rem; }
        h1 { color: #2c3e50; }
        .metric-label { font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🍞 Florio Produtos Alimentícios | Dashboard Empresarial")

p = [
    "GRISSINI PARMESÃO", "GRISSINI PIZZA", "PÃO SUECO INTEGRAL", "CROUTON ALHO", "TORRADA AZEITONAS PRETAS",
    "CROSTINI TOMATE SECO", "BISCOITO QUEIJO CURADO", "PALITO GERGELIM", "TORRADA MULTIGRÃOS", "PÃO SUECO TRADICIONAL",
    "GRISSINI ALECRIM", "CROUTON ERVAS FINAS", "TORRADA CEBOLA E SALSA"
]

def g_df():
    d = []
    for i in range(90):
        dia = datetime.now() - timedelta(days=i)
        for prod in p:
            v = random.randint(10, 180)
            pr = round(random.uniform(5.5, 16.0), 2)
            rec = round(v * pr, 2)
            fix = round(random.uniform(300, 800), 2)
            var = round(rec * random.uniform(0.4, 0.65), 2)
            lucro = rec - (fix + var)
            d.append([dia.date(), prod, v, pr, rec, fix, var, lucro])
    return pd.DataFrame(d, columns=["Data", "Produto", "Vendas", "Preco", "Receita", "Custo Fixo", "Custo Variavel", "Lucro"])

df = g_df()

st.sidebar.header("Filtros")
ini = st.sidebar.date_input("Data Início", df["Data"].min())
fim = st.sidebar.date_input("Data Fim", df["Data"].max())
prod_sel = st.sidebar.multiselect("Produtos", p, default=p)

filt = df[(df["Data"] >= ini) & (df["Data"] <= fim) & (df["Produto"].isin(prod_sel))]

tv = filt["Vendas"].sum()
tr = filt["Receita"].sum()
tl = filt["Lucro"].sum()

c1, c2, c3 = st.columns(3)
c1.metric("📦 Unidades Vendidas", f"{tv}")
c2.metric("💰 Receita Total", f"R$ {tr:,.2f}")
c3.metric("📈 Lucro Total", f"R$ {tl:,.2f}")

st.subheader("🔎 Vendas por Produto")
fig1 = px.bar(filt.groupby("Produto")["Vendas"].sum().reset_index(), x="Produto", y="Vendas", color="Produto", text_auto=True)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📆 Receita Diária")
fig2 = px.area(filt.groupby("Data")["Receita"].sum().reset_index(), x="Data", y="Receita")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("💵 Fluxo de Caixa")
fc = filt.groupby("Data")[["Receita", "Custo Fixo", "Custo Variavel", "Lucro"]].sum().reset_index()
fig3 = px.line(fc, x="Data", y=["Receita", "Custo Fixo", "Custo Variavel", "Lucro"], markers=True)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📊 Dados Detalhados")
st.dataframe(filt, use_container_width=True)

st.markdown("---")
st.caption("Desenvolvido para Florio Produtos Alimentícios | 2025")
