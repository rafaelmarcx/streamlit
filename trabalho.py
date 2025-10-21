import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Controle de Produção das Máquinas")


st.sidebar.header("Carregar Dados")
arquivo = st.sidebar.file_uploader("Escolha um arquivo CSV", type=["csv"])

if arquivo:
    dados = pd.read_csv(arquivo)
else:
    st.warning("Carregue um arquivo CSV para começar.")
    st.stop()


st.subheader("Dados de Produção")
st.dataframe(dados)


st.sidebar.header("Adicionar Novo Registro")
with st.sidebar.form("novo_registro"):
    data = st.date_input("Data")
    maquina = st.text_input("Máquina")
    turno = st.selectbox("Turno", ["Manhã", "Tarde", "Noite"])
    produzidas = st.number_input("Peças Produzidas", min_value=0)
    defeituosas = st.number_input("Peças Defeituosas", min_value=0)
    adicionar = st.form_submit_button("Adicionar")

if adicionar:
    novo = {
        "data": data,
        "maquina": maquina,
        "turno": turno,
        "produzidas": produzidas,
        "defeituosas": defeituosas
    }
    dados = pd.concat([dados, pd.DataFrame([novo])], ignore_index=True)
    st.success("Novo registro adicionado com sucesso!")


st.sidebar.header("Filtros")
maquinas = st.sidebar.multiselect("Máquina", dados["maquina"].unique())
turnos = st.sidebar.multiselect("Turno", dados["turno"].unique())

filtrado = dados.copy()
if maquinas:
    filtrado = filtrado[filtrado["maquina"].isin(maquinas)]
if turnos:
    filtrado = filtrado[filtrado["turno"].isin(turnos)]


filtrado["boas"] = filtrado["produzidas"] - filtrado["defeituosas"]
filtrado["eficiencia"] = (filtrado["boas"] / filtrado["produzidas"]) * 100


media_ef = filtrado["eficiencia"].mean()
media_prod = filtrado["produzidas"].mean()

st.metric("Eficiência Média (%)", f"{media_ef:.1f}")
st.metric("Produção Média por Máquina", f"{media_prod:.1f}")


if media_ef < 90:
    st.error("Eficiência média abaixo de 90%!")
if media_prod < 80:
    st.warning("Produção média abaixo de 80 peças por dia!")


st.subheader("Produção Diária por Máquina")
fig1 = px.bar(filtrado, x="data", y="produzidas", color="maquina", barmode="group")
st.plotly_chart(fig1)


st.subheader("Taxa de Defeitos (%)")
filtrado["taxa_defeitos"] = (filtrado["defeituosas"] / filtrado["produzidas"]) * 100
fig2 = px.line(filtrado, x="data", y="taxa_defeitos", color="maquina")
st.plotly_chart(fig2)


st.download_button(
    "Baixar CSV",
    data=filtrado.to_csv(index=False).encode("utf-8"),
    file_name="dados_producao.csv",
    mime="text/csv"
)
