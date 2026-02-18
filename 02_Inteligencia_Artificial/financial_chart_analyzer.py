import google.generativeai as genai
import PIL.Image

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
genai.configure(api_key=MINHA_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 1. CARREGAR O GRÁFICO ---
imagem_path = 'grafico_vendas.jpg' # <--- Verifique se o nome está igual ao que você salvou
print(f"📊 Lendo o arquivo visual: {imagem_path}...")

try:
    imagem_grafico = PIL.Image.open(imagem_path)
except:
    print("❌ Erro: Não achei a imagem. Salvou na pasta certa?")
    exit()

# --- 2. O PROMPT DE "REVERSE ENGINEERING" ---
prompt_analista = """
Você é um Analista Sênior de BI.
Analise este gráfico/dashboard detalhadamente.

TAREFA 1 - INSIGHTS:
- Identifique a tendência principal (crescimento, queda, sazonalidade).
- Aponte o pico máximo e o vale mínimo (se houver).
- Há alguma anomalia visível?

TAREFA 2 - EXTRAÇÃO DE DADOS (REVERSE ENGINEERING):
- Estime os valores numéricos de cada ponto do gráfico.
- Gere uma tabela em formato CSV (Mês/Periodo, Valor Estimado).
"""

# --- 3. EXECUÇÃO ---
print("🤖 Processando pixels e extraindo matemática...")
response = model.generate_content([prompt_analista, imagem_grafico])

print("\n" + "="*40)
print("RELATÓRIO DO ANALISTA IA:")
print("="*40)
print(response.text)