import streamlit as st
import pandas as pd

# Carregar o arquivo Excel
df = pd.read_excel("Acompanhamento de Contrato - COGEPRO - Coordenadoria de Gerenciamento de Programas e Projetos.xlsx", sheet_name="Contratos", skiprows=1)

st.set_page_config(layout="wide")
st.title("📊 Dashboard de Acompanhamento de Contratos - COGEPRO")

# Exibir colunas carregadas (útil para debug)
st.write("🧾 Colunas encontradas:", df.columns.tolist())

# Buscar automaticamente a coluna que contém 'contrato'
col_nome_contrato = [col for col in df.columns if "contrato" in col.lower()][0]

# Corrigir tipo das colunas de percentual
df["% Executado"] = pd.to_numeric(df["Unnamed: 53"], errors="coerce")
df["% Financeiro"] = pd.to_numeric(df["Unnamed: 54"], errors="coerce")

# Filtros dinâmicos
tipo_opcao = st.selectbox("Filtrar por Tipo de Contrato", options=["Todos"] + sorted(df["Tipo"].dropna().unique().tolist()))
recurso_opcao = st.selectbox("Filtrar por Recurso", options=["Todos"] + sorted(df["Recurso"].dropna().astype(str).unique().tolist()))

df_filtrado = df.copy()
if tipo_opcao != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo_opcao]
if recurso_opcao != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Recurso"].astype(str) == recurso_opcao]

# Mostrar dados filtrados
st.subheader("📑 Lista de Contratos")
st.dataframe(df_filtrado[[col_nome_contrato, "Tipo", "Data da \\nAssinatura", "Objeto", "% Executado", "% Financeiro", "Recurso"]], use_container_width=True)

# Gráfico
st.subheader("📈 Execução Física e Financeira")
st.bar_chart(df_filtrado[["% Executado", "% Financeiro"]].dropna())
