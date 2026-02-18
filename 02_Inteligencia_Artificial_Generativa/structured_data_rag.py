import google.generativeai as genai
import pandas as pd
import random

# --- 1. CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
genai.configure(api_key=MINHA_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. CARREGANDO OS DADOS REAIS (ETAPA DE ENGENHARIA DE DADOS) ---
print("📂 Carregando base de produtos...")
try:
    # Lê o arquivo que você criou
    df = pd.read_csv('produtos_1000_precos_realistas.csv')
    
    # TRUQUE: Vamos forçar 10 produtos aleatórios a terem ESTOQUE 0 para testar o bot
    produtos_zerados = random.sample(range(len(df)), 10)
    df.loc[produtos_zerados, 'estoque'] = 0
    
    # Mostra no terminal quais foram zerados pra você saber o que testar
    print("\n🔻 PRODUTOS COM ESTOQUE ZERADO (PARA TESTE):")
    print(df.loc[produtos_zerados, ['nome', 'estoque']])
    print("-" * 50)

except FileNotFoundError:
    print("❌ ERRO: O arquivo 'produtos_1000_precos_realistas.csv' não foi encontrado.")
    print("Dica: Verifique se o nome está igual e se está na mesma pasta do script.")
    exit()

# --- 3. FUNÇÃO DE BUSCA (RAG COM PANDAS) ---
def consultar_estoque(termo_busca):
    termo_busca = termo_busca.lower()
    
    # Busca inteligente: Procura o termo no NOME ou na CATEGORIA
    # (É como dar um Ctrl+F no Excel)
    filtro = df['nome'].str.lower().str.contains(termo_busca) | \
             df['categoria'].str.lower().str.contains(termo_busca)
    
    resultados = df[filtro]
    
    # Se não achou nada
    if resultados.empty:
        return ""
    
    # Se achou, converte as linhas encontradas para texto
    # Limitamos a 5 produtos para não gastar muitos tokens se a busca for genérica
    texto_resposta = ""
    for index, linha in resultados.head(5).iterrows():
        texto_resposta += f"- ID: {linha['id']} | Nome: {linha['nome']} | Categoria: {linha['categoria']} | Preço: R$ {linha['preco']:.2f} | Estoque: {linha['estoque']} | Descrição: {linha['descricao']}\n"
    
    return texto_resposta

# --- 4. O CHATBOT VENDEDOR ---
chat = model.start_chat(history=[])

print("\n🛒 SISTEMA J&P MODAS ONLINE (Baseado em CSV)")
print("Dica: Pergunte sobre 'Vestido', 'Camiseta' ou use os nomes que apareceram zerados acima.")
print("Digite 'sair' para encerrar.\n")

while True:
    pergunta = input("Você: ")
    if pergunta.lower() == "sair":
        break
        
    # Busca no Pandas
    dados_csv = consultar_estoque(pergunta)
    
    # Se o Pandas não achou nada relevante, a gente avisa a IA para ela não alucinar
    if not dados_csv:
        contexto = "O sistema de busca não encontrou nenhum produto com esse nome exato."
    else:
        contexto = f"DADOS ENCONTRADOS NO CSV:\n{dados_csv}"

    # Prompt
    prompt = f"""
    Você é um Vendedor Consultivo de um grande varejista de moda.
    
    {contexto}
    
    REGRAS:
    1. Use APENAS os dados acima para responder.
    2. Se o estoque for 0, diga que está esgotado e ofereça outro similar se houver na lista.
    3. Se encontrar vários produtos, liste as opções com preços.
    4. Se não tiver dados, peça para o cliente refinar a busca (ex: 'Pode ser mais específico?').
    
    PERGUNTA DO CLIENTE: {pergunta}
    """
    
    try:
        response = chat.send_message(prompt)
        print(f"🤖 IA: {response.text}\n")
    except Exception as e:
        print(f"Erro: {e}")
        