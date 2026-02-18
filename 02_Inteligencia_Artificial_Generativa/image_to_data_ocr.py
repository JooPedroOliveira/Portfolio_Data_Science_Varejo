import google.generativeai as genai
import PIL.Image
import json
import pandas as pd

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
genai.configure(api_key=MINHA_API_KEY)

# --- 1. CARREGAR A IMAGEM  ---
img_path = 'roupa_teste.jpg'
try:
    imagem = PIL.Image.open(img_path)
except:
    print(f"❌ Erro: Não achei {img_path}")
    exit()

# --- 2. CONFIGURAR O MODELO PARA JSON ---
# Aqui está o segredo: avisamos que a saída TEM que ser JSON
model = genai.GenerativeModel('gemini-2.5-flash',
                              generation_config={"response_mime_type": "application/json"})

# --- 3. PROMPT DE ENGENHARIA DE DADOS ---
# Note que eu peço explicitamente a estrutura das chaves (keys)
prompt = """
Analise esta imagem de produto de moda.
Extraia os dados técnicos para cadastro em ERP.
Responda usando este esquema JSON exato:
{
  "nome_produto": "string",
  "categoria": "string",
  "cor_principal": "string",
  "detalhes": ["lista", "de", "detalhes"],
  "publico_alvo": "string (Masculino/Feminino/Unissex/Infantil)",
  "vibe_estilo": "string (ex: Casual, Formal, Streetwear)"
}
"""

print(f"🔄 Processando imagem '{img_path}' para extração de dados...")

try:
    # Chama a API
    response = model.generate_content([prompt, imagem])
    
    # --- 4. TRATAMENTO DOS DADOS (O "ETL") ---
    # A resposta vem como texto JSON, convertemos para Dicionário Python
    dados_dict = json.loads(response.text)
    
    print("\n✅ DADOS BRUTOS (JSON) RECEBIDOS DA IA:")
    print(json.dumps(dados_dict, indent=4, ensure_ascii=False))
    
    # --- 5. SALVAR EM EXCEL/CSV (A Mágica do BI) ---
    # Convertemos o dicionário para um DataFrame (Tabela)
    # Precisamos colocar [dados_dict] entre colchetes pq é uma linha só
    df_novo = pd.DataFrame([dados_dict])
    
    # Salvamos num arquivo novo
    nome_arquivo = "novos_cadastros.csv"
    
    # O mode='a' significa APPEND (adicionar no fim se já existir)
    # header=False se o arquivo já existir (para não repetir cabeçalho)
    df_novo.to_csv(nome_arquivo, index=False, sep=';', encoding='utf-8-sig')
    
    print(f"\n💾 Sucesso! Dados salvos no arquivo '{nome_arquivo}'.")
    print("Abra esse arquivo no Excel para conferir a tabulação.")

except Exception as e:
    print(f"❌ Erro: {e}")