import google.generativeai as genai
import pandas as pd

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
genai.configure(api_key=MINHA_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 1. CARREGAR OS DADOS JÁ TRATADOS ---
# Vamos ler o arquivo que a IA gerou na aula anterior
arquivo = 'relatorio_nps_analisado.csv'

print(f"📊 Lendo base de inteligência: {arquivo}...")
try:
    # sep=';' porque salvamos assim na aula anterior
    df = pd.read_csv(arquivo, sep=';', encoding='utf-8-sig')
    
    # Transformamos a tabela em texto para a IA ler
    # (Como a base é pequena, podemos passar tudo. Se fosse gigante, enviaríamos só o resumo)
    tabela_texto = df.to_markdown(index=False)
    
except FileNotFoundError:
    print("❌ Erro: Rode a Aula 8 primeiro para gerar o arquivo!")
    exit()

# --- 2. O PROMPT DO DIRETOR (RAG ANALÍTICO) ---
prompt_estrategico = f"""
Você é o Head de Customer Experience (CX) de um grande varejista.
Abaixo estão os dados reais dos últimos feedbacks dos clientes, já classificados.

DADOS DO RELATÓRIO:
{tabela_texto}

SUA MISSÃO:
Analise esses dados e gere um **Relatório Executivo** para a Diretoria contendo:

1.  **Diagnóstico Principal:** Qual é a maior dor do cliente hoje? (Cite % se possível).
2.  **Análise de Causa Raiz:** Nos casos de Logística/Produto, o que exatamente está acontecendo?
3.  **Destaques Positivos:** O que estamos fazendo certo para replicar?
4.  **PLANO DE AÇÃO IMEDIATO:** Sugira 3 ações práticas para resolver os problemas críticos levantados.

Formate a resposta de forma profissional e direta.
"""

# --- 3. GERAR O RELATÓRIO ---
print("🧠 A IA está analisando os padrões e redigindo o relatório...")
response = model.generate_content(prompt_estrategico)

print("\n" + "="*50)
print("📄 RELATÓRIO EXECUTIVO DE CX")
print("="*50)
print(response.text)

# Opcional: Salvar o relatório em texto
with open("Relatorio_Diretoria.txt", "w", encoding="utf-8") as f:
    f.write(response.text)
print("\n💾 Relatório salvo em 'Relatorio_Diretoria.txt'")