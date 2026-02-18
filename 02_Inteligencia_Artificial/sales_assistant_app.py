import google.generativeai as genai
import chromadb
import time

# ==============================================================================
# ⚙️ CONFIGURAÇÃO DO APP
# ==============================================================================
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"

# Modelos de elite
MODELO_CHAT = "models/gemini-2.5-flash" 
MODELO_EMBEDDING = "models/gemini-embedding-001"

genai.configure(api_key=MINHA_API_KEY)
modelo_inteligente = genai.GenerativeModel(MODELO_CHAT)

# Conecta no MESMO banco que o ETL criou
print("🔌 Conectando ao Banco de Dados Enterprise...")
chroma_client = chromadb.PersistentClient(path="banco_vetorial_jp_modas")
collection = chroma_client.get_collection(name="estoque_vip_jp_modas")

total_produtos = collection.count()
print(f"✅ Sistema Online! {total_produtos} produtos disponíveis no estoque.")

# ==============================================================================
# 🤖 LOOP DO VENDEDOR
# ==============================================================================
print("\n" + "="*60)
print(f"👔 VENDEDOR VIRTUAL J&P MODAS (Gemini 2.5 Pro)")
print("="*60)

while True:
    pergunta = input("\n👤 Cliente: ")
    if pergunta.lower() in ["sair", "fim"]:
        print("👋 Até logo!")
        break

    print("🔎 Procurando as melhores opções...")
    
    try:
        # 1. Busca Semântica (Retrieval)
        # Aqui usamos o embedding só para a pergunta (1 token, super barato)
        vetor_pergunta = genai.embed_content(model=MODELO_EMBEDDING, content=pergunta)["embedding"]
        
        # Traz os 4 produtos mais relevantes
        resultados = collection.query(query_embeddings=[vetor_pergunta], n_results=4)
        
        # 2. Montagem do Contexto (Grounding)
        contexto = ""
        # Verifica se achou algo
        if not resultados['ids'][0]:
            print("❌ Não encontrei produtos similares.")
            continue

        for i in range(len(resultados['ids'][0])):
            item = resultados['documents'][0][i]
            meta = resultados['metadatas'][0][i]
            contexto += f"- {item} | Preço: R$ {meta['preco']:.2f}\n"

        # 3. Geração da Resposta (Generation)
        prompt = f"""
        Você é um Personal Stylist e Vendedor Sênior de um grande varejista de moda.
        
        PERFIL DO CLIENTE (O que ele pediu): "{pergunta}"
        
        OPÇÕES DISPONÍVEIS NO ESTOQUE:
        {contexto}
        
        SUA MISSÃO:
        Recomende a melhor opção da lista acima para este cliente.
        Use uma linguagem persuasiva, elegante e simpática (use emojis).
        Justifique a escolha conectando a descrição do produto com o desejo do cliente.
        Se o cliente perguntou algo fora do contexto de roupa, diga gentilmente que só vende moda.
        """
        
        response = modelo_inteligente.generate_content(prompt)
        print(f"\n🤖 Gemini 2.5 Pro:\n{response.text}")
        
    except Exception as e:
        print(f"❌ Erro temporário: {e}")
        print("Dica: Se for erro 429, espere 1 minuto e tente de novo.")