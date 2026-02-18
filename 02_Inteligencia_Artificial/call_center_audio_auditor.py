import google.generativeai as genai
import time
import json

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
MODELO_AUDIO = "models/gemini-2.5-flash" 

genai.configure(api_key=MINHA_API_KEY)

# ==============================================================================
# 🎧 FUNÇÃO DE UPLOAD (Mandar o MP3 pro Google)
# ==============================================================================
def processar_audio(caminho_arquivo):
    print(f"📤 Enviando áudio '{caminho_arquivo}' para análise...")
    
    # 1. Faz o upload do arquivo para o servidor temporário do Gemini
    arquivo_audio = genai.upload_file(caminho_arquivo, mime_type="audio/mp3")
    
    # 2. Espera o processamento (arquivos grandes demoram uns segundos)
    while arquivo_audio.state.name == "PROCESSING":
        print("   Processando...", end="\r")
        time.sleep(1)
        arquivo_audio = genai.get_file(arquivo_audio.name)
        
    print("✅ Áudio pronto para análise!")
    return arquivo_audio

# ==============================================================================
# 🧠 O CÉREBRO AUDITOR
# ==============================================================================
def auditar_atendimento(arquivo_audio):
    model = genai.GenerativeModel(
        MODELO_AUDIO,
        system_instruction="Você é o Supervisor de Qualidade do Call Center da J&P Modas."
    )
    
    prompt = """
    Ouça atentamente esta gravação de suporte ao cliente.
    
    SUA MISSÃO:
    1. Transcreva o resumo do problema.
    2. Identifique o sentimento do cliente (Raiva, Tristeza, Feliz, Neutro).
    3. Identifique se o cliente ameaçou alguma ação legal (Procon/Processo).
    4. Dê uma nota de 0 a 10 para a gravidade do caso.
    
    SAÍDA JSON OBRIGATÓRIA:
    {
        "resumo_problema": "Texto",
        "sentimento_cliente": "Texto",
        "risco_juridico": true/false,
        "gravidade_0_10": numero,
        "plano_acao": "O que o supervisor deve fazer?"
    }
    """
    
    print("👂 A IA está ouvindo a gravação...")
    # Mágica: Enviamos o prompt + o objeto de áudio
    response = model.generate_content(
        [prompt, arquivo_audio],
        generation_config={"response_mime_type": "application/json"}
    )
    
    return json.loads(response.text)

# ==============================================================================
# 🚀 EXECUÇÃO
# ==============================================================================
print("\n" + "="*60)
print("🎧 J&P VOICE INTELLIGENCE - AUDITORIA DE SAC")
print("="*60)

# ⚠️ IMPORTANTE: Tenha um arquivo 'reclamacao.mp3' na pasta!
arquivo_teste = "reclamacao.mp3" 

try:
    # Passo 1: Carrega
    audio_ref = processar_audio(arquivo_teste)
    
    # Passo 2: Analisa
    resultado = auditar_atendimento(audio_ref)
    
    # Passo 3: Relatório
    print("\n📋 RELATÓRIO DE QUALIDADE:")
    print(f"😡 Sentimento: {resultado['sentimento_cliente'].upper()}")
    print(f"🔥 Gravidade: {resultado['gravidade_0_10']}/10")
    print(f"⚖️ Risco Jurídico: {'SIM! ALERTA!' if resultado['risco_juridico'] else 'Não'}")
    print(f"📝 Resumo: {resultado['resumo_problema']}")
    print(f"👮 Ação Sugerida: {resultado['plano_acao']}")

except Exception as e:
    print(f"❌ Erro (Você criou o arquivo mp3?): {e}")