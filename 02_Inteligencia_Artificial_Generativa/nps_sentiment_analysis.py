import google.generativeai as genai
import pandas as pd
import time

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
genai.configure(api_key=MINHA_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 1. CARREGAR DADOS (MODO MANUAL BLINDADO) ---
print("📥 Carregando reviews dos clientes...")
try:
    # Passo 1: Lemos o arquivo como texto puro, linha por linha
    with open('reviews_clientes.csv', 'r', encoding='utf-8-sig') as f:
        linhas = f.readlines()
    
    # Passo 2: Limpamos cada linha na mão
    dados_limpos = []
    for linha in linhas:
        # .strip() tira o \n (enter) do final
        # .strip('"') tira as aspas do começo e fim da linha (O SEGREDO!)
        linha_limpa = linha.strip().strip('"')
        
        # .split(';', 2) quebra a linha nos primeiros 2 pontos-e-vírgula
        # O '2' garante que se tiver um ';' no meio do comentário, ele não quebra errado!
        dados_limpos.append(linha_limpa.split(';', 2))

    # Passo 3: Transformamos essa lista limpa em DataFrame do Pandas
    colunas = dados_limpos[0] # A primeira linha é o cabeçalho
    conteudo = dados_limpos[1:] # O resto é dado
    
    df = pd.DataFrame(conteudo, columns=colunas)
    
    # Garantia extra: remove espaços dos nomes das colunas
    df.columns = df.columns.str.strip()
    
    print(f"✅ Sucesso! Colunas identificadas: {df.columns.tolist()}")
    
    # Verificação final
    if 'comentario_cliente' not in df.columns:
        print("❌ ALERTA: Coluna 'comentario_cliente' não encontrada.")
        print("Colunas atuais:", df.columns)
        exit()

except Exception as e:
    print(f"❌ Erro fatal: {e}")
    exit()

# --- 2. FUNÇÃO DE CLASSIFICAÇÃO (A "Mente" do BI) ---
def analisar_review(comentario):
    prompt = f"""
    Você é um Analista de Qualidade Sênior de um varejista de moda.
    Analise o comentário do cliente abaixo.
    
    COMENTÁRIO: "{comentario}"
    
    TAREFA:
    Classifique este feedback em 3 categorias exatas.
    
    SAÍDA ESPERADA (Responda APENAS neste formato, separado por PIPE '|'):
    SENTIMENTO|CATEGORIA_PRINCIPAL|RESUMO_CURTO
    
    Regras de Categoria:
    - Logística (Atraso, entrega errada)
    - Produto (Qualidade, tamanho, tecido)
    - Financeiro (Preço, cobrança indevida, estorno)
    - Usabilidade (Site travou, app confuso, UX)
    - Atendimento (Loja física, suporte)
    
    Exemplo de Resposta:
    Negativo|Logística|Entrega atrasada
    """
    
    try:
        response = model.generate_content(prompt)
        # Limpa o texto para garantir que não venha sujeira
        return response.text.strip()
    except:
        return "Erro|Erro|Erro na API"

# --- 3. PROCESSAMENTO EM LOTE (O "ETL") ---
print(f"📊 Processando {len(df)} comentários... Isso pode levar alguns segundos.")

# Criamos listas vazias para guardar os resultados
sentimentos = []
categorias = []
resumos = []

for index, row in df.iterrows():
    comentario = row['comentario_cliente']
    print(f"🔄 Analisando ID {row['id_review']}...", end="\r")
    
    # Chama a IA
    resultado_ia = analisar_review(comentario)
    
    # Quebra a resposta da IA (SENTIMENTO|CATEGORIA|RESUMO)
    try:
        partes = resultado_ia.split('|')
        sentimentos.append(partes[0].strip())
        categorias.append(partes[1].strip())
        resumos.append(partes[2].strip())
    except:
        # Se a IA falhar no formato, preenchemos com "N/A"
        sentimentos.append("Indefinido")
        categorias.append("Outros")
        resumos.append("Formato inválido")
    
    # Pausa de segurança para não estourar o limite gratuito (opcional no pago)
    time.sleep(1) 

# --- 4. SALVAR RESULTADO NO PANDAS ---
df['Sentimento_IA'] = sentimentos
df['Categoria_Raiz'] = categorias
df['Motivo'] = resumos

print("\n✅ Análise Concluída! Veja uma amostra:")
print(df[['comentario_cliente', 'Sentimento_IA', 'Categoria_Raiz']].head(10))

# Exportar para Excel (Pronto para o Power BI)
arquivo_final = "relatorio_nps_analisado.csv"
df.to_csv(arquivo_final, sep=';', index=False, encoding='utf-8-sig')
print(f"\n💾 Arquivo '{arquivo_final}' gerado com sucesso!")