import google.generativeai as genai
import PIL.Image

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
genai.configure(api_key=MINHA_API_KEY)

# --- 1. CARREGAR A IMAGEM ---
print("📸 Carregando a imagem...")
try:
    # Substitua pelo nome da sua imagem se for diferente
    imagem_roupa = PIL.Image.open('roupa_teste.jpg') 
except FileNotFoundError:
    print("❌ Erro: Não achei o arquivo 'roupa_teste.jpg'. Colocou na pasta certa?")
    exit()

# --- 2. O PROMPT DE ENGENHARIA DE DADOS ---
# Aqui pedimos para ele agir como um Especialista em Cadastro de Produto
model = genai.GenerativeModel('gemini-2.5-flash')

prompt_vision = """
Analise esta imagem tecnicamente para cadastro no sistema de E-commerce da J&P MODAS.
Extraia as seguintes informações em formato de lista:

1. Tipo de Peça (ex: Camiseta, Calça, Vestido)
2. Cor Predominante
3. Tipo de Estampa (se houver)
4. Detalhes de Modelagem (ex: Manga longa, Gola V, Skinny)
5. Sugestão de Ocasião de Uso (ex: Casual, Festa, Trabalho)
6. Uma descrição curta e vendedora para o site (máximo 2 linhas).

Seja técnico e preciso.
"""

# --- 3. ENVIAR TEXTO + IMAGEM JUNTOS ---
print("🤖 Analisando visualmente...")
response = model.generate_content([prompt_vision, imagem_roupa])

print("\n" + "="*40)
print("FICHA TÉCNICA GERADA:")
print("="*40)
print(response.text)