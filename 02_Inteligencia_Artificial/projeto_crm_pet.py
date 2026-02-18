import google.generativeai as genai
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
genai.configure(api_key=MINHA_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 1. CARGA E ANÁLISE DE DADOS (BI PURO) ---
print("📊 Carregando base de vendas...")
try:
    # 1. Tenta ler com separador ';'. Se falhar, o Python avisa.
    # 2. O encoding='utf-8-sig' resolve problemas de acentuação do Excel.
    df = pd.read_csv('vendas_marketplace.csv', sep=';', encoding='utf-8-sig')
    
    # TRUQUE DE MESTRE: Limpar nomes das colunas (remove espaços extras que o Excel cria)
    df.columns = df.columns.str.strip()
    
    # DEBUG: Mostra para você como o Python leu as colunas
    print("Colunas lidas:", df.columns.tolist())

    # --- CORREÇÃO DA DATA (O Pulo do Gato) ---
    # dayfirst=True avisa: "Python, o primeiro número é o DIA, não o mês!"
    # errors='coerce' diz: "Se tiver uma data zuada, ignora e deixa em branco, mas não trava".
    df['data_ultima_compra'] = pd.to_datetime(df['data_ultima_compra'], dayfirst=True, errors='coerce')
    
    # Se tiver preço com vírgula (ex: 1500,00), converte para ponto
    if df['total_gasto'].dtype == 'O': # Se leu como texto
        df['total_gasto'] = df['total_gasto'].str.replace(',', '.').astype(float)

    # Data de referência
    hoje = datetime(2026, 2, 15)
    
    # Calcular RECÊNCIA
    df['dias_sem_comprar'] = (hoje - df['data_ultima_compra']).dt.days

    # --- LÓGICA DE SEGMENTAÇÃO RFM (Simplificada) ---
    def classificar_cliente(row):
        if row['dias_sem_comprar'] > 90:
            return "Churn (Perdido)"
        elif row['dias_sem_comprar'] > 30 and row['qtde_compras'] > 5:
            return "Risco de Abandono (Urgente)" # Era fiel e parou
        elif row['qtde_compras'] == 1 and row['dias_sem_comprar'] < 30:
            return "Novo Cliente"
        elif row['qtde_compras'] > 10:
            return "Campeão (Vip)"
        else:
            return "Cliente Recorrente"

    df['status_crm'] = df.apply(classificar_cliente, axis=1)
    
    print("\n📋 CLASSIFICAÇÃO DA CARTEIRA:")
    print(df[['nome_cliente', 'dias_sem_comprar', 'produto_favorito', 'status_crm']])

except FileNotFoundError:
    print("Erro: Crie o arquivo 'vendas_marketplace.csv' antes!")
    exit()

# --- 2. A MÁGICA DA IA (GERAÇÃO DE AÇÃO) ---
print("\n🤖 Gerando estratégias de recuperação para o Site Próprio...\n")

# Vamos iterar por cada cliente e criar a mensagem personalizada
for index, cliente in df.iterrows():
    
    nome = cliente['nome_cliente']
    produto = cliente['produto_favorito']
    status = cliente['status_crm']
    dias = cliente['dias_sem_comprar']

    # Prompt Dinâmico: Muda de acordo com o status do cliente
    prompt_marketing = f"""
    Você é o Gerente de CRM da 'PetShop Amigo'.
    O cliente {nome} está com o status: {status}.
    Ele costuma comprar: {produto}.
    Faz {dias} dias que ele não compra.
    
    OBJETIVO: Fazer ele comprar no nosso NOVO SITE PRÓPRIO (www.petamigo.com.br) e sair do Mercado Livre.
    
    REGRAS:
    1. Crie uma mensagem curta para WhatsApp (máximo 2 frases).
    2. Se for 'Risco de Abandono', ofereça um cupom agressivo 'VOLTA15'.
    3. Se for 'Campeão', convide para o Clube de Assinatura com desconto.
    4. Se for 'Novo', agradeça e dê cupom de primeira compra no site.
    5. Cite o produto favorito dele para gerar conexão.
    
    Gere apenas a mensagem.
    """

    try:
        response = model.generate_content(prompt_marketing)
        print(f"👤 {nome} ({status}) | Produto: {produto}")
        print(f"💬 ZAP: {response.text}")
        print("-" * 50)
    except:
        print("Erro na API")