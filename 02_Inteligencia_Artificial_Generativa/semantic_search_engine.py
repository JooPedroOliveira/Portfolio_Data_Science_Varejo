import google.generativeai as genai
import numpy as np
import pandas as pd

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
genai.configure(api_key=MINHA_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 1. A BASE DE CONHECIMENTO ---
documentos = [
    {
        "titulo": "Troca de Roupa Íntima",
        "conteudo": "Por questões de higiene e saúde, não realizamos troca de peças íntimas (calcinhas, cuecas), exceto em caso de defeito de fabricação comprovado."
    },
    {
        "titulo": "Prazo de Entrega Expresso",
        "conteudo": "A entrega expressa está disponível para capitais e ocorre em até 24 horas úteis após a aprovação do pagamento. O custo é calculado no checkout."
    },
    {
        "titulo": "Política de Reembolso PIX",
        "conteudo": "Compras pagas via PIX são reembolsadas na mesma conta de origem em até 2 horas após a confirmação da devolução no centro de distribuição."
    },
    {
        "titulo": "Clube J&P MODAS e Vantagens",
        "conteudo": "Membros do programa de fidelidade ganham 10% de desconto na primeira compra do mês e acesso antecipado a coleções exclusivas."
    }
]

df = pd.DataFrame(documentos)

# --- 2. CRIANDO OS EMBEDDINGS (VERSÃO COMPATÍVEL) ---
def gerar_embedding(texto):
    # Removemos o 'task_type' para evitar conflitos com versões diferentes de modelos
    return genai.embed_content(
        model="models/gemini-embedding-001", 
        content=texto
    )["embedding"]

print("🧮 Vetorizando a base de conhecimento (Indexação)...")
try:
    df['vetor'] = df['conteudo'].apply(gerar_embedding)
    print("✅ Base indexada! Cada texto agora é uma lista de números.")
except Exception as e:
    print(f"❌ Erro na vetorização: {e}")
    exit()

# --- 3. SISTEMA DE BUSCA ---
def buscar_melhor_resposta(pergunta_usuario):
    # 1. Vetoriza a pergunta
    vetor_pergunta = genai.embed_content(
        model="models/gemini-embedding-001",
        content=pergunta_usuario
    )["embedding"]
    
    # 2. Matemática: Produto Escalar
    produtos_escalares = []
    
    for vetor_doc in df['vetor']:
        score = np.dot(vetor_pergunta, vetor_doc)
        produtos_escalares.append(score)
    
    df['score_similaridade'] = produtos_escalares
    df_ordenado = df.sort_values('score_similaridade', ascending=False)
    
    melhor_doc = df_ordenado.iloc[0]
    return melhor_doc

# --- 4. INTERFACE DO CHATBOT ---
print("\n🤖 CHATBOT ENTERPRISE (Baseado em Vetores)")
print("Este bot lê apenas o parágrafo necessário, economizando 99% de tokens.")

while True:
    pergunta = input("\nPergunta: ")
    if pergunta.lower() == "sair":
        break
        
    try:
        # Passo A: O "Retrieval"
        doc_encontrado = buscar_melhor_resposta(pergunta)
        
        print(f"   [DEBUG] Tópico Recuperado: '{doc_encontrado['titulo']}' (Score: {doc_encontrado['score_similaridade']:.4f})")
        
        # Passo B: A Geração
        prompt = f"""
        Você é um assistente virtual. Responda à pergunta do usuário usando APENAS o contexto abaixo.
        
        CONTEXTO OFICIAL:
        {doc_encontrado['conteudo']}
        
        PERGUNTA: {pergunta}
        """
        
        response = model.generate_content(prompt)
        print(f"🤖 Resposta: {response.text}")
        
    except Exception as e:
        print(f"Erro na execução: {e}")