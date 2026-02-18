import google.generativeai as genai
import os

# --- 1. CONFIGURAÇÃO ---
# Cole sua API KEY aqui
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
genai.configure(api_key=MINHA_API_KEY)

# Usamos o Flash porque ele é rápido e barato para ler textos longos
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. O CONTEXTO (GROUNDING) ---
# Isso é o que chamamos de "A Verdade da Empresa".
# A IA não pode inventar nada fora disso.
politica_j_p_modas = """
POLÍTICA DE TROCAS E DEVOLUÇÕES - J&P MODAS

1. PRAZO GERAL: O cliente pode trocar qualquer peça de vestuário em até 30 dias com a etiqueta afixada.
2. TROCA EM LOJA: Compras do site podem ser trocadas em qualquer loja física.
3. RESTRIÇÕES DE HIGIENE (IMPORTANTE):
   - NÃO aceitamos troca ou devolução de: Calcinhas, Cuecas, Sungas, Biquínis e Brincos.
   - Exceção única: Se a peça íntima apresentar defeito de fabricação comprovado.
4. ESTADO DA PEÇA: Peças lavadas, usadas ou com odores não serão aceitas.
"""

# --- 3. O CENÁRIO (O CLIENTE) ---
# O cliente vai tentar "dar um migué", dizendo que só provou.
duvida_cliente = """
Oi, boa tarde. Comprei um kit de calcinhas de algodão semana passada.
Chegou ontem, eu provei uma só por cima da roupa e ficou apertada.
As outras 4 do kit nem toquei. Quero trocar o kit todo por um tamanho maior.
Como faço?
"""

# --- 4. O PROMPT DE ENGENHARIA (A INSTRUÇÃO) ---
prompt_blindado = f"""
Você é um Assistente de Atendimento Sênior de um grande varejista de moda.
Sua tarefa é responder ao cliente baseando-se ESTRITAMENTE na política abaixo.

REGRAS DE OURO:
1. Seja educado e empático, mas FIRME nas regras.
2. Se a política proibir, você DEVE dizer NÃO.
3. Não invente exceções que não estão escritas.

POLÍTICA INTERNA:
{politica_j_p_modas}

MENSAGEM DO CLIENTE:
{duvida_cliente}
"""

# --- 5. EXECUÇÃO ---
print("🛒 Analisando solicitação do cliente...")
response = model.generate_content(prompt_blindado)

print("\n" + "="*40)
print("RESPOSTA DO BOT:")
print("="*40)
print(response.text)