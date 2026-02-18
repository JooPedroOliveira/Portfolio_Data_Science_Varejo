import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==============================================================================
# 🎨 CONFIGURAÇÃO DA PÁGINA (LAYOUT)
# ==============================================================================
st.set_page_config(
    page_title="J&P - War Room de Vendas",
    page_icon="🛍️",
    layout="wide" # Usa a tela inteira
)

# Título e Subtítulo
st.title("🛍️ J&P Modas - Recuperação de Vendas com IA")
st.markdown("---")

# ==============================================================================
# 📂 CARREGAMENTO DE DADOS
# ==============================================================================
arquivo_dados = "disparos_hoje.csv"

# Função com cache para não carregar toda hora se o arquivo for gigante
@st.cache_data
def carregar_dados():
    if os.path.exists(arquivo_dados):
        # Lê o CSV gerado na aula anterior (com separador ;)
        return pd.read_csv(arquivo_dados, sep=';')
    else:
        return None

df = carregar_dados()

# ==============================================================================
# 🚨 TRATAMENTO DE ERRO (CASO O ARQUIVO NÃO EXISTA)
# ==============================================================================
if df is None:
    st.error("⚠️ Arquivo de dados não encontrado!")
    st.info("Por favor, rode o script da Aula 14 primeiro para gerar o 'disparos_hoje.csv'.")
    st.stop() # Para a execução aqui

# ==============================================================================
# 📊 KPIs (INDICADORES DE DESEMPENHO)
# ==============================================================================
# Tratamento simples de dados
df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce') # Garante que é número

# Cálculos
total_recuperavel = df['Valor'].sum()
ticket_medio = df['Valor'].mean()
total_clientes = len(df)
estrategia_top = df['Acao_Tomada'].mode()[0] if not df.empty else "N/A"

# Exibição em Colunas (Cards)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Potencial de Receita", f"R$ {total_recuperavel:,.2f}")
with col2:
    st.metric("👥 Clientes na Fila", total_clientes)
with col3:
    st.metric("🏷️ Ticket Médio", f"R$ {ticket_medio:,.2f}")
with col4:
    st.metric("🧠 Estratégia Favorita da IA", estrategia_top)

st.markdown("---")

# ==============================================================================
# 📈 GRÁFICOS INTERATIVOS (PLOTLY)
# ==============================================================================
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("🎯 Estratégias Definidas pela IA")
    # Gráfico de Pizza
    fig_pizza = px.pie(df, names='Acao_Tomada', title='Distribuição de Ações (Ofertas)', hole=0.4)
    st.plotly_chart(fig_pizza, use_container_width=True)

with col_graf2:
    st.subheader("💰 Valor por Cliente")
    # Gráfico de Barras
    fig_barras = px.bar(df, x='Cliente', y='Valor', color='Acao_Tomada', title='Quem são os maiores carrinhos?')
    st.plotly_chart(fig_barras, use_container_width=True)

# ==============================================================================
# 📑 TABELA DETALHADA E FILTROS
# ==============================================================================
st.subheader("📋 Detalhe Operacional (Fila de Disparo)")

# Filtro Lateral (Sidebar)
st.sidebar.header("Filtros")
filtro_acao = st.sidebar.multiselect(
    "Filtrar por Ação da IA:",
    options=df['Acao_Tomada'].unique(),
    default=df['Acao_Tomada'].unique()
)

# Aplica o filtro
df_filtrado = df[df['Acao_Tomada'].isin(filtro_acao)]

# Mostra a tabela interativa
st.dataframe(
    df_filtrado,
    use_container_width=True,
    column_config={
        "Valor": st.column_config.NumberColumn(format="R$ %.2f"),
        "Mensagem_Enviada": "Mensagem WhatsApp (IA)"
    },
    hide_index=True
)

# ==============================================================================
# 🔘 BOTÃO DE AÇÃO
# ==============================================================================
st.sidebar.markdown("---")
st.sidebar.write("### 🚀 Painel de Controle")

if st.sidebar.button("DISPARAR WHATSAPP AGORA 📲"):
    # Aqui entraria a conexão com Twilio/Zenvia
    barra = st.sidebar.progress(0)
    import time
    for i in range(100):
        time.sleep(0.02)
        barra.progress(i + 1)
    
    st.sidebar.success(f"✅ {len(df_filtrado)} mensagens enviadas com sucesso!")
    st.balloons() # Efeito visual de comemoração