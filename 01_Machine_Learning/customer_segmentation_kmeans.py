import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings

warnings.filterwarnings('ignore')

# ==============================================================================
# 1. GERAÇÃO DE DADOS TRANSACIONAIS (O CAOS REAL)
# ==============================================================================
# Diferente dos outros, aqui geramos COMPRAS soltas, não o resumo do cliente.
# O desafio é transformar "Linhas de Nota Fiscal" em "Perfil de Cliente".
np.random.seed(42)
n_transacoes = 10000
n_clientes = 1000

print("🎲 Gerando 10.000 transações de compras aleatórias...")

# IDs de clientes (alguns compram muito, outros pouco)
cliente_ids = np.random.randint(1, n_clientes + 1, n_transacoes)

# Datas (últimos 365 dias)
datas = pd.date_range(end=pd.Timestamp.now(), periods=365).tolist()
data_compra = np.random.choice(datas, n_transacoes)

# Valores (Regra de Pareto: poucos gastam muito)
valores = np.random.exponential(scale=200, size=n_transacoes) + 20 # Mínimo R$ 20

df_transacoes = pd.DataFrame({
    'id_cliente': cliente_ids,
    'data_compra': data_compra,
    'valor': valores
})

print(f"📊 Base Bruta: {len(df_transacoes)} vendas realizadas.")

# ==============================================================================
# 2. ENGENHARIA DE FEATURES (RFM - Recency, Frequency, Monetary)
# ==============================================================================
# Aqui transformamos o caos em inteligência.
# R (Recência): Quantos dias faz que ele não compra? (Menor é melhor)
# F (Frequência): Quantas vezes comprou? (Maior é melhor)
# M (Monetário): Quanto gastou no total? (Maior é melhor)

ultima_data = df_transacoes['data_compra'].max()

df_rfm = df_transacoes.groupby('id_cliente').agg({
    'data_compra': lambda x: (ultima_data - x.max()).days, # Recência
    'id_cliente': 'count',                                 # Frequência
    'valor': 'sum'                                         # Monetário
}).rename(columns={
    'data_compra': 'Recencia',
    'id_cliente': 'Frequencia',
    'valor': 'Monetario'
})

print("\n📋 Perfil RFM dos Clientes (Primeiras 5 linhas):")
print(df_rfm.head())

# ==============================================================================
# 3. PRÉ-PROCESSAMENTO (STANDARD SCALER É OBRIGATÓRIO AQUI!)
# ==============================================================================
# Por que escalar?
# Recência vai de 0 a 365 dias. Monetário vai de 0 a R$ 10.000.
# Sem escalar, o K-Means vai achar que o dinheiro é 100x mais importante que os dias.
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(df_rfm)

# ==============================================================================
# 4. DEFININDO O NÚMERO DE GRUPOS (MÉTODO DO COTOVELO / ELBOW)
# ==============================================================================
# Como é não-supervisionado, não sabemos se existem 3, 4 ou 10 tipos de clientes.
# A IA vai testar e nos dizer onde o erro "quebra" (o cotovelo).

erro_wcss = []
range_k = range(1, 11) # Testa de 1 a 10 grupos

print("\n💪 Calculando o 'Cotovelo' para achar o número ideal de grupos...")
for k in range_k:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(rfm_scaled)
    erro_wcss.append(kmeans.inertia_) # Inertia = quão bagunçados estão os grupos
    # ... (o loop for k in range_k que você já tem)

print("\n📉 A TABELA DA DECISÃO (ELBOW METHOD):")
print(f"{'GRUPOS (K)':<10} | {'BAGUNÇA (INERTIA)':<20} | {'QUANTO MELHOROU?'}")
print("-" * 50)

ultimo_erro = 0
for i, erro in enumerate(erro_wcss):
    k = i + 1
    diferenca = ultimo_erro - erro if k > 1 else 0
    print(f"{k:<10} | {erro:<20.0f} | -{diferenca:.0f}")
    ultimo_erro = erro

print("-" * 50)
print("💡 DICA: Pare quando a 'Melhora' começar a ficar pequena.")

# Matematicamente, vamos escolher 4 grupos para este exemplo (é um padrão bom pro varejo)
k_ideal = 4
model = KMeans(n_clusters=k_ideal, random_state=42, n_init=10)
clusters = model.fit_predict(rfm_scaled)

# Adiciona o resultado na tabela original
df_rfm['Cluster'] = clusters

# ==============================================================================
# ==============================================================================
# 5. ANÁLISE DE NEGÓCIO (QUEM É QUEM?) - BLOCO CORRIGIDO
# ==============================================================================
print("\n" + "="*60)
print(f"🕵️‍♂️ ANÁLISE DOS {k_ideal} GRUPOS ENCONTRADOS")
print("="*60)

# 1. Agrupa e calcula as médias
analise_grupos = df_rfm.groupby('Cluster').agg({
    'Recencia': 'mean',
    'Frequencia': 'mean',
    'Monetario': ['mean', 'count']
}).round(0)

# 2. CORREÇÃO DO ERRO: Achatamos os nomes das colunas na força bruta
# Assim garantimos que não existem "tuplas" ou "multi-index" para confundir o código
analise_grupos.columns = ['Media_Dias_Sem_Comprar', 'Media_Compras_Ano', 'Media_Gasto_Total', 'Qtd_Clientes']

# 3. Agora a função usa os nomes simples que definimos acima
def nomear_cluster(row):
    r = row['Media_Dias_Sem_Comprar']
    f = row['Media_Compras_Ano']
    m = row['Media_Gasto_Total']
    
    # Ajustando a régua para a realidade dos dados gerados
    if m > 2500: # Baixei de 3000 para 2500
        return "💎 CAMPEÕES (VIPs)"
    elif r > 90 and m > 1000: # Baixei recência para 90 dias (3 meses já é risco)
        return "⚠️ EM RISCO (Gastavam bem e sumiram)"
    elif r > 90: # Baixei para 90 dias
        return "💤 HIBERNANDO"
    elif f > 5:
        return "🌱 PROMESSAS (Novos e ativos)"
    else:
        return "👤 CLIENTE PADRÃO"

# Aplica a função
analise_grupos['Perfil'] = analise_grupos.apply(nomear_cluster, axis=1)

# Ordena por quem gasta mais
print(analise_grupos.sort_values('Media_Gasto_Total', ascending=False))

print("\n" + "="*60)
print("🚀 ESTRATÉGIAS SUGERIDAS PARA O CRM")
print("="*60)

for index, row in analise_grupos.iterrows():
    perfil = row['Perfil']
    print(f"\nGrupo {index}: {perfil}")
    if "CAMPEÕES" in perfil:
        print("   -> Ação: Concierge Exclusivo, Convite para eventos, Acesso antecipado.")
    elif "EM RISCO" in perfil:
        print("   -> Ação: Cupom agressivo AGORA! Ligar para entender o problema.")
    elif "HIBERNANDO" in perfil:
        print("   -> Ação: Email marketing automático de reativação (baixo custo).")
    elif "PROMESSAS" in perfil:
        print("   -> Ação: Oferecer cartão fidelidade para aumentar o ticket médio.")
    else:
        print("   -> Ação: Comunicação padrão de ofertas semanais.")
        # ==============================================================================
# 6. CÁLCULO DE UPLIFT FINANCEIRO (O "CHEQUE")
# ==============================================================================
print("\n" + "="*60)
print("💰 CALCULADORA DE POTENCIAL FINANCEIRO (UPLIFT)")
print("="*60)

# 1. Definir quem vamos atacar (Grupos Críticos)
# Vamos somar a quantidade de clientes que cairam nos perfis de resgate
qtd_risco = analise_grupos[analise_grupos['Perfil'].str.contains('RISCO')]['Qtd_Clientes'].sum()
qtd_hibernando = analise_grupos[analise_grupos['Perfil'].str.contains('HIBERNANDO')]['Qtd_Clientes'].sum()
total_alvo_campanha = qtd_risco + qtd_hibernando

# 2. Calcular o Ticket Médio Geral da empresa (para estimar quanto eles gastariam)
ticket_medio_estimado = df_transacoes['valor'].mean()

# 3. Premissas de Conversão (Isso você ajusta conforme a realidade da C&A)
taxa_conversao_sem_ia = 0.005  # 0.5% (E-mail genérico que ninguém abre)
taxa_conversao_com_ia = 0.05   # 5.0% (Cupom agressivo + Alvo certo)

# 4. A Matemática do Lucro
receita_passiva = total_alvo_campanha * taxa_conversao_sem_ia * ticket_medio_estimado
receita_com_ia = total_alvo_campanha * taxa_conversao_com_ia * ticket_medio_estimado
uplift = receita_com_ia - receita_passiva

print(f"🎯 Público Alvo da Campanha (Risco + Hibernando): {total_alvo_campanha} clientes")
print(f"💵 Ticket Médio Esperado: R$ {ticket_medio_estimado:.2f}")
print("-" * 60)

print(f"📉 Cenário Sem Ação (Conversão {taxa_conversao_sem_ia*100}%):")
print(f"   R$ {receita_passiva:,.2f}")

print(f"📈 Cenário Com IA (Conversão {taxa_conversao_com_ia*100}%):")
print(f"   R$ {receita_com_ia:,.2f}")

print("-" * 60)
print(f"🚀 DINHEIRO NOVO NA MESA (UPLIFT): R$ {uplift:,.2f}")
print("=" * 60)