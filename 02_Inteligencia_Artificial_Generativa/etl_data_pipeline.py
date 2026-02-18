import google.generativeai as genai
import pandas as pd
import chromadb
import time
import os

# ==============================================================================
# ⚙️ CONFIGURAÇÃO DE ENGENHARIA
# ==============================================================================
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"

# Modelo de Vetor (O único que importa para este arquivo)
MODELO_EMBEDDING = "models/gemini-embedding-001"

genai.configure(api_key=MINHA_API_KEY)

# Conecta ao DISCO (Salva na pasta 'banco_vetorial_enterprise')
chroma_client = chromadb.PersistentClient(path="banco_vetorial_jp_modas")
collection = chroma_client.get_or_create_collection(name="estoque_vip_jp_modas")

# ==============================================================================
# 📥 PROCESSO DE CARGA (BATCH / LOTES)
# ==============================================================================
def executar_etl():
    arquivo_csv = 'produtos_1000_precos_realistas.csv'
    
    # 1. Garante que o CSV existe
    if not os.path.exists(arquivo_csv):
        print("⚠️ CSV não encontrado. Gerando dados simulados...")
        df_fake = pd.DataFrame({'id': range(1, 1001), 
                                'nome': [f'Produto {i}' for i in range(1, 1001)],
                                'categoria': ['Moda']*1000,
                                'descricao': ['Descrição teste']*1000,
                                'preco': [99.90]*1000})
        df_fake.to_csv(arquivo_csv, index=False)

    df = pd.read_csv(arquivo_csv)
    total_csv = len(df)
    
    print(f"🏭 INICIANDO ETL (CARGA DE DADOS)...")
    print(f"📊 Total no CSV: {total_csv}")
    print(f"💾 Total já no Banco: {collection.count()}")

    if collection.count() < total_csv:
        print(f"🚀 Iniciando processamento em LOTES DE 50 (Economia de API)...")
        
        ids_lote, docs_lote, meta_lote = [], [], []
        TAMANHO_LOTE = 50 # O segredo da economia
        
        for index, row in df.iterrows():
            id_str = str(row['id'])
            
            # Checagem rápida local (não gasta API)
            if len(collection.get(ids=[id_str])['ids']) > 0:
                continue

            # Prepara dados
            texto_produto = f"{row['nome']} - {row['categoria']} - {row['descricao']}"
            
            ids_lote.append(id_str)
            docs_lote.append(texto_produto)
            meta_lote.append({"preco": float(row['preco']), "categoria": row['categoria']})
            
            # --- DISPARA A API SÓ QUANDO O LOTE ENCHE ---
            if len(ids_lote) >= TAMANHO_LOTE:
                try:
                    print(f"⚡ Enviando lote de {len(ids_lote)} itens...", end='\r')
                    
                    # Gera 50 vetores de uma vez só
                    resultado = genai.embed_content(
                        model=MODELO_EMBEDDING,
                        content=docs_lote
                    )
                    
                    # Salva no ChromaDB
                    collection.add(
                        ids=ids_lote,
                        documents=docs_lote,
                        embeddings=resultado['embedding'],
                        metadatas=meta_lote
                    )
                    
                    print(f"✅ Lote salvo! Progresso: {index+1}/{total_csv}      ")
                    
                    # Reseta listas e descansa a API
                    ids_lote, docs_lote, meta_lote = [], [], []
                    time.sleep(2) 
                    
                except Exception as e:
                    print(f"\n❌ Erro no lote: {e}")
                    print("⏳ Esperando 30s por segurança...")
                    time.sleep(30)

        # Processa o último lote (se sobrou algo)
        if ids_lote:
            try:
                print("⚡ Salvando lote final...")
                res = genai.embed_content(model=MODELO_EMBEDDING, content=docs_lote)
                collection.add(ids=ids_lote, documents=docs_lote, embeddings=res['embedding'], metadatas=meta_lote)
                print("✅ ETL CONCLUÍDO COM SUCESSO!")
            except Exception as e:
                print(f"Erro final: {e}")

    else:
        print("⚡ O banco já está 100% atualizado. Nenhuma ação necessária.")

if __name__ == "__main__":
    executar_etl()