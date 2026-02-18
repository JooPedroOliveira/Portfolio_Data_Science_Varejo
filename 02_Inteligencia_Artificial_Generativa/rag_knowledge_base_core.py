import google.generativeai as genai

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
genai.configure(api_key=MINHA_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- NOSSO "BANCO DE DADOS" ---
estoque_jp_modas = {
    "calça jeans skinny": {"preco": 99.90, "estoque": 15, "cor": "azul"},
    "camiseta básica": {"preco": 29.90, "estoque": 0, "cor": "branca"},
    "tênis casual": {"preco": 149.90, "estoque": 5, "cor": "preto"},
    "jaqueta couro fake": {"preco": 299.90, "estoque": 2, "cor": "preta"}
}

def consultar_sistema(pergunta_usuario):
    pergunta_usuario = pergunta_usuario.lower()
    
    # Criamos uma lista para guardar tudo que encontrarmos
    resultados = []
    
    for item_estoque in estoque_jp_modas:
        # Se a palavra 'camiseta' estiver dentro de 'camiseta básica', ele encontra!
        if pergunta_usuario in item_estoque or item_estoque in pergunta_usuario:
            dados = estoque_jp_modas[item_estoque]
            resultados.append(f"PRODUTO: {item_estoque} | PREÇO: R$ {dados['preco']} | ESTOQUE: {dados['estoque']} | COR: {dados['cor']}")
    
    # Se encontrou algo, junta tudo em um texto só
    if resultados:
        return "\n".join(resultados)
    
    return "Produto não encontrado no catálogo."

# --- INICIALIZANDO O CHAT COM A "ALMA" DO VENDEDOR ---
# Aqui a gente já diz quem ela é logo no início
chat = model.start_chat(history=[])

print("--- 🤖 VENDEDOR J&P MODAS SENIOR (Com Memória e Regras) ---")

while True:
    pergunta_usuario = input("\nVocê: ")

    if pergunta_usuario.lower() == "sair":
        break

    # 1. Busca informação no sistema
    contexto_recuperado = consultar_sistema(pergunta_usuario)

    # 2. O seu Prompt de Vendedor (O cérebro de negócio voltou!)
    prompt_final = f"""
    Você é um vendedor digital de um grande varejista de moda focado em conversão de vendas.
    
    DADOS ATUAIS DO SISTEMA:
    {contexto_recuperado}

    SUAS REGRAS DE OURO:
    1. Se o estoque for 0, seja honesto, mas ofereça algo similar ou peça para o cliente assinar o 'avise-me'.
    2. Se tiver estoque, valorize o produto (ex: 'Essa jaqueta está super em alta!').
    3. Use o histórico da nossa conversa para entender referências como 'e esse?', 'qual o mais caro?'.
    4. Nunca invente preços que não estão nos dados do sistema.

    PERGUNTA DO CLIENTE: {pergunta_usuario}
    """

    # 3. Envia para a IA
    try:
        response = chat.send_message(prompt_final)
        print(f"\n🤖 IA: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")