import google.generativeai as genai

# --- CONFIGURAÇÃO DA J&P ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
MODELO_ESCOLHIDO = "models/gemini-2.5-flash" # Sua escolha campeã!

genai.configure(api_key=MINHA_API_KEY)

# ==============================================================================
# 🛠️ AS "MÃOS" DA IA (FERRAMENTAS/FUNÇÕES)
# ==============================================================================
# Aqui definimos funções Python normais.
# Num cenário real, elas consultariam APIs de verdade.

def consultar_frete(cep: str):
    """
    Calcula o valor do frete e o prazo de entrega para um determinado CEP.
    Args:
        cep: O CEP do cliente (ex: 12345-678).
    """
    print(f"\n   [SISTEMA J&P] 🚚 Consultando API de Transportadora para {cep}...")
    
    # Simulação de lógica de negócio
    if cep.startswith("0"):
        return {"valor": 15.90, "prazo": "1 dia útil (Expresso SP)", "transportadora": "Loggi"}
    elif cep.startswith("2"):
        return {"valor": 22.50, "prazo": "3 dias úteis", "transportadora": "Correios"}
    else:
        return {"valor": 35.00, "prazo": "5 a 7 dias úteis", "transportadora": "Total Express"}

def verificar_estoque_tempo_real(produto: str, tamanho: str):
    """
    Verifica se existe estoque físico disponível no armazém da J&P agora.
    Args:
        produto: Nome do produto (ex: Camiseta, Tênis).
        tamanho: Tamanho desejado (P, M, G, 40, 42).
    """
    print(f"\n   [SISTEMA J&P] 🏭 Verificando estoque no SAP para {produto} tam {tamanho}...")
    
    # Simulação
    if "P" in tamanho or "38" in tamanho:
        return {"disponivel": False, "msg": "Esgotado no momento."}
    else:
        return {"disponivel": True, "quantidade": 45, "msg": "Em estoque pronta entrega."}

def aplicar_cupom_desconto(cupom: str):
    """
    Valida se um cupom de desconto é válido na J&P.
    Args:
        cupom: O código do cupom (ex: VERAO10).
    """
    print(f"\n   [SISTEMA J&P] 🎟️ Validando cupom '{cupom}' no banco de dados...")
    
    cupom = cupom.upper().strip()
    if cupom == "JP10":
        return {"valido": True, "desconto": "10%", "tipo": "Primeira Compra"}
    elif cupom == "FRETEZERO":
        return {"valido": True, "desconto": "Frete Grátis", "tipo": "Campanha Relâmpago"}
    else:
        return {"valido": False, "msg": "Cupom expirado ou inválido."}

# ==============================================================================
# 🧠 CONFIGURANDO O CÉREBRO COM ACESSO ÀS FERRAMENTAS
# ==============================================================================

# 1. Colocamos as funções numa lista
minhas_ferramentas = [consultar_frete, verificar_estoque_tempo_real, aplicar_cupom_desconto]

# 2. Avisamos o Gemini: "Olha, você pode usar essas ferramentas se precisar"
# O parametro 'tools' faz a mágica acontecer automaticamente (Automatic Function Calling)
chat = genai.GenerativeModel(
    MODELO_ESCOLHIDO,
    tools=minhas_ferramentas
).start_chat(enable_automatic_function_calling=True)

# ==============================================================================
# 🤖 INTERFACE DO CLIENTE J&P
# ==============================================================================
print("\n" + "="*50)
print(f"🛍️ ATENDIMENTO J&P (Agente Autônomo Ativado)")
print("="*50)
print("Dica: Pergunte sobre frete para o CEP 01000, ou estoque de Camiseta G, ou tente o cupom JP10.")

while True:
    msg = input("\n👤 Cliente: ")
    if msg.lower() in ["sair", "fim"]:
        print("👋 J&P agradece a preferência!")
        break

    try:
        # Enviamos a mensagem para o chat.
        # Se o Gemini perceber que precisa de uma ferramenta, ele PAUSA,
        # RODA a função Python (você verá o print [SISTEMA J&P]),
        # PEGA o resultado e GERA a resposta final. Tudo sozinho.
        response = chat.send_message(msg)
        print(f"🤖 J&P: {response.text}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")