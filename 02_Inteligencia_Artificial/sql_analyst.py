import sqlite3
import google.generativeai as genai
import pandas as pd

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
# Usando o 2.5 Flash (Rápido e bom de código)
MODELO_SQL = "models/gemini-2.5-flash" 

genai.configure(api_key=MINHA_API_KEY)

# ==============================================================================
# 🗄️ PARTE 1: CRIANDO O DATA WAREHOUSE DA J&P (SIMULAÇÃO)
# ==============================================================================
def criar_banco_dados():
    # Conecta num banco na memória (RAM), some quando fecha o script
    conn = sqlite3.connect(':memory:') 
    cursor = conn.cursor()
    
    # 1. Tabela de Produtos
    cursor.execute('''
    CREATE TABLE produtos (
        id_produto INTEGER PRIMARY KEY,
        nome TEXT,
        categoria TEXT,
        custo REAL,
        preco_venda REAL
    )''')
    
    # 2. Tabela de Vendas
    cursor.execute('''
    CREATE TABLE vendas (
        id_venda INTEGER PRIMARY KEY,
        data_venda DATE,
        id_produto INTEGER,
        quantidade INTEGER,
        estado_cliente TEXT,
        canal_venda TEXT
    )''')
    
    # Inserindo dados fictícios (Carga Inicial)
    produtos = [
        (1, 'Camiseta Básica', 'Vestuário', 15.0, 49.90),
        (2, 'Calça Jeans Premium', 'Vestuário', 45.0, 199.90),
        (3, 'Tênis Running', 'Calçados', 80.0, 399.90),
        (4, 'Boné J&P', 'Acessórios', 10.0, 59.90),
        (5, 'Relógio Digital', 'Acessórios', 50.0, 150.00)
    ]
    cursor.executemany('INSERT INTO produtos VALUES (?,?,?,?,?)', produtos)
    
    vendas = [
        (101, '2026-02-01', 1, 2, 'SP', 'Site'),
        (102, '2026-02-02', 2, 1, 'RJ', 'App'),
        (103, '2026-02-02', 3, 1, 'SP', 'Loja Física'),
        (104, '2026-02-03', 1, 5, 'MG', 'Site'),
        (105, '2026-02-04', 4, 2, 'SP', 'App'),
        (106, '2026-02-05', 3, 2, 'RS', 'Site'),
        (107, '2026-02-05', 2, 3, 'SP', 'Loja Física'),
        (108, '2026-02-06', 5, 10, 'BA', 'Revenda') # Venda grande
    ]
    cursor.executemany('INSERT INTO vendas VALUES (?,?,?,?,?,?)', vendas)
    
    conn.commit()
    return conn

# ==============================================================================
# 🧠 PARTE 2: O CÉREBRO QUE ESCREVE SQL (Text-to-SQL)
# ==============================================================================
def perguntar_aos_dados(pergunta, conexao):
    model = genai.GenerativeModel(MODELO_SQL)
    
    # O SEGREDO: Passar o esquema (mapa) do banco para a IA
    prompt_sistema = """
    Você é um Engenheiro de Dados Sênior especialista em SQL (SQLite).
    
    ESQUEMA DO BANCO DE DADOS:
    1. Tabela 'produtos': id_produto, nome, categoria, custo, preco_venda
    2. Tabela 'vendas': id_venda, data_venda, id_produto, quantidade, estado_cliente, canal_venda
    
    SUA MISSÃO:
    Converta a pergunta do usuário em uma Query SQL válida.
    
    REGRAS:
    - Retorne APENAS o código SQL. Sem markdown (```), sem explicações. Comece direto com SELECT.
    - Se precisar de faturamento, calcule: SUM(vendas.quantidade * produtos.preco_venda).
    - Faça os JOINs necessários entre 'vendas' e 'produtos' usando id_produto.
    
    PERGUNTA DO USUÁRIO:
    """
    
    try:
        # Gera o SQL
        resposta = model.generate_content(f"{prompt_sistema} {pergunta}")
        query_sql = resposta.text.replace("```sql", "").replace("```", "").strip()
        
        print(f"\n📝 SQL Gerado pela IA:\n{query_sql}")
        
        # Executa o SQL no banco
        df_resultado = pd.read_sql_query(query_sql, conexao)
        return df_resultado
        
    except Exception as e:
        return f"Erro ao processar: {e}"

# ==============================================================================
# 🚀 PARTE 3: INTERFACE DO DIRETOR
# ==============================================================================
conn = criar_banco_dados()

print("\n" + "="*60)
print("📊 ANALISTA DE DADOS ROBÔ J&P (Text-to-SQL)")
print("="*60)
print("Pergunte coisas como:")
print(" - Qual o faturamento total?")
print(" - Qual estado comprou mais?")
print(" - Qual produto vendeu mais quantidade?")
print(" - Liste as vendas do canal Site")

while True:
    pergunta = input("\n👤 Diretor pergunta: ")
    if pergunta.lower() in ["sair", "fim"]:
        conn.close()
        break
    
    resultado = perguntar_aos_dados(pergunta, conn)
    
    if isinstance(resultado, pd.DataFrame):
        if resultado.empty:
            print("📭 Nenhum dado encontrado para essa pergunta.")
        else:
            print("\n📈 RESULTADO:")
            # Truque para formatar dinheiro se tiver coluna de valor
            print(resultado.to_markdown(index=False))
            
            # Bônus: A IA explica o número (Data Storytelling)
            # Poderíamos adicionar uma chamada extra aqui para a IA comentar o resultado
    else:
        print(f"❌ {resultado}")