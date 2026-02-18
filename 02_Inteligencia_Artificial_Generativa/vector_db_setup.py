import google.generativeai as genai
import pandas as pd
import chromadb
from chromadb.config import Settings

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
genai.configure(api_key=MINHA_API_KEY)

# --- 1. CONFIGURANDO O BANCO VETORIAL (PERSISTENTE) ---
# Isso cria uma pasta 'banco_vetorial_ca' no seu computador.
# Os dados ficam salvos lá para sempre!
chroma_client = chromadb.PersistentClient(path="banco_vetorial_jp_modas")

# Criamos uma "coleção" (é como se fosse uma Tabela SQL)
nome_colecao = "produtos_jp_modas"

# O get_or_create garante que não vamos apagar dados se rodarmos de novo
collection = chroma_client.get_or_create_collection(name=nome_colecao)

# --- 2. FUNÇÃO DE EMBEDDING (GEMINI) ---
def gerar_embedding(texto):
    try:
        return genai.embed_content(
            model="models/gemini-embedding-001", # O modelo que funcionou pra você
            content=texto
        )["embedding"]
    except Exception as e:
        print(f"Erro ao vetorizar: {e}")
        return []

# --- 3. INGESTÃO DE DADOS (ETL) ---
# Vamos verificar se o banco já está cheio para não duplicar
if collection.count() == 0:
    print("📂 Banco vazio! Iniciando carga de dados do CSV...")
    
    # Lendo o CSV que você criou
    df = pd.read_csv('produtos_1000_precos_realistas.csv')
    
    # Para o teste ser rápido, vamos carregar apenas os primeiros 20 produtos
    # Num cenário real, faríamos um loop no milhão de linhas
    df_amostra = df.head(20) 
    
    ids = []
    documentos = [] # O texto que será buscado
    metadados = [] # Dados extras (preço, categoria) para filtrar depois
    vetores = []
    
    print("⏳ Gerando vetores (Isso pode levar alguns segundos)...")
    for index, row in df_amostra.iterrows():
        # Criamos um "texto rico" para a IA entender o produto
        texto_produto = f"{row['nome']} - {row['categoria']} - {row['descricao']}"
        
        # Geramos a matemática
        vetor = gerar_embedding(texto_produto)
        
        if vetor:
            ids.append(str(row['id']))
            documentos.append(texto_produto)
            metadados.append({"preco": row['preco'], "categoria": row['categoria']})
            vetores.append(vetor)
            print(f"   Processado: {row['nome']}")

    # Salvando tudo no ChromaDB de uma vez (Batch Insert)
    collection.add(
        ids=ids,
        documents=documentos,
        embeddings=vetores,
        metadatas=metadados
    )
    print(f"✅ Sucesso! {len(ids)} produtos indexados no ChromaDB.")

else:
    print(f"⚡ Banco carregado! Total de documentos: {collection.count()}")


# --- 4. O MOTOR DE BUSCA (SEARCH ENGINE) ---
print("\n🔍 MOTOR DE BUSCA SEMÂNTICA J&P MODAS")
print("Dica: Tente buscar por 'roupa para festa' ou 'algo confortável'.")

while True:
    query = input("\nO que você procura? (ou 'sair'): ")
    if query.lower() == "sair":
        break
    
    # 1. Vetorizamos a pergunta do usuário
    vetor_pergunta = gerar_embedding(query)
    
    # 2. O Chroma faz a busca matemática super rápida
    resultados = collection.query(
        query_embeddings=[vetor_pergunta],
        n_results=3 # Traz os 3 melhores
    )
    
    # 3. Exibição dos Resultados
    print("\n🎯 PRODUTOS ENCONTRADOS:")
    
    # O Chroma retorna listas dentro de listas, então precisamos iterar
    for i in range(len(resultados['ids'][0])):
        id_prod = resultados['ids'][0][i]
        texto = resultados['documents'][0][i]
        meta = resultados['metadatas'][0][i]
        distancia = resultados['distances'][0][i] # Quanto menor, mais similar
        
        print(f"   🛒 [{id_prod}] {texto}")
        print(f"      Preço: R$ {meta['preco']} | Categoria: {meta['categoria']}")
        print("-" * 40)