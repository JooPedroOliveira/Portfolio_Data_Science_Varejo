import google.generativeai as genai
import pandas as pd
import json
import time

# --- CONFIGURAÇÃO ---
MINHA_API_KEY = "INSIRA_SUA_CHAVE_AQUI"
# Usando o Flash que é gratuito e rápido
MODELO_ESCOLHIDO = "models/gemini-2.5-flash" 

genai.configure(api_key=MINHA_API_KEY)

# ==============================================================================
# 🎲 SIMULADOR DE DADOS (O que viria da API da Loja/Analytics)
# ==============================================================================
def buscar_carrinhos_abandonados():
    print("📡 Conectando ao CRM da J&P Modas...")
    time.sleep(1)
    
    # Lista simulada de clientes que abandonaram o checkout hoje
    dados_reais = [
        {
            "id_cliente": 105,
            "nome": "Fernanda Lima",
            "carrinho": ["Vestido Longo Floral", "Sandália Anabela"],
            "valor": 459.90,
            "tempo_abandono": "45 minutos",
            "origem_trafego": "Instagram Ads",
            "comportamento": "Viu a página de frete e saiu."
        },
        {
            "id_cliente": 208,
            "nome": "Carlos Mendes",
            "carrinho": ["Tênis Esportivo Pro", "Meias Performance", "Boné"],
            "valor": 899.90,
            "tempo_abandono": "2 dias",
            "origem_trafego": "Google Orgânico",
            "comportamento": "Cliente recorrente (já comprou 3x). Visitou o carrinho 5 vezes."
        },
        {
            "id_cliente": 310,
            "nome": "Amanda Souza",
            "carrinho": ["Blusa Básica Branca"],
            "valor": 49.90,
            "tempo_abandono": "1 hora",
            "origem_trafego": "Direto",
            "comportamento": "Novo usuário. Tentou usar cupom inválido."
        }
    ]
    print(f"✅ Encontrados {len(dados_reais)} carrinhos para recuperar.\n")
    return dados_reais

# ==============================================================================
# 🧠 O CÉREBRO (AGENTE RECUPERADOR)
# ==============================================================================
def analisar_cliente(dados):
    # Configuramos o modelo para responder APENAS JSON
    model = genai.GenerativeModel(
        MODELO_ESCOLHIDO,
        generation_config={"response_mime_type": "application/json"}
    )

    prompt = f"""
    Você é o Agente de Recuperação de Vendas da J&P (Faturamento 500k/mês).
    Analise este caso de carrinho abandonado e decida a abordagem.
    
    DADOS DO CLIENTE:
    {json.dumps(dados, indent=2, ensure_ascii=False)}
    
    REGRAS DE NEGÓCIO:
    1. Frete caro? Ofereça FRETE GRÁTIS se o valor > 200.
    2. Cliente VIP (recorrente)? Não dê desconto, ofereça atendimento VIP/Consultoria.
    3. Cupom inválido? Envie um cupom que funciona (BEMVINDO10).
    4. Ticket alto (>500)? Abordagem consultiva, sem parecer robô.
    5. Ticket baixo? Cupom agressivo para fechar logo.
    
    SAÍDA JSON OBRIGATÓRIA:
    {{
        "diagnostico": "Por que ele não comprou?",
        "estrategia": "Qual o gatilho mental (Urgência/Vantagem/VIP)?",
        "oferta": "O que vamos dar? (Cupom/Frete/Nada)",
        "mensagem_zap": "O texto curto e persuasivo para enviar no WhatsApp agora."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return {"erro": str(e)}

# ==============================================================================
# 🚀 EXECUÇÃO DO FLUXO
# ==============================================================================
print("="*60)
print("💰 RECUPERADOR AUTOMÁTICO J&P - SISTEMA ENTERPRISE")
print("="*60)

carrinhos = buscar_carrinhos_abandonados()
relatorio_final = []

for cliente in carrinhos:
    print(f"🤖 Analisando: {cliente['nome']} (R$ {cliente['valor']})...")
    
    decisao_ia = analisar_cliente(cliente)
    
    # Junta os dados para salvar
    linha = {
        "Cliente": cliente['nome'],
        "Valor": cliente['valor'],
        "Diagnostico_IA": decisao_ia.get('diagnostico'),
        "Acao_Tomada": decisao_ia.get('oferta'),
        "Mensagem_Enviada": decisao_ia.get('mensagem_zap')
    }
    relatorio_final.append(linha)
    
    # Mostra na tela bonitinho
    print(f"   🎯 Estratégia: {decisao_ia.get('estrategia')}")
    print(f"   📱 WhatsApp: \"{decisao_ia.get('mensagem_zap')}\"")
    print("-" * 50)
    time.sleep(1)

# Salva o arquivo para o time de atendimento
df = pd.DataFrame(relatorio_final)
df.to_csv("disparos_hoje.csv", index=False, sep=';', encoding='utf-8-sig')
print("\n✅ Processo finalizado! Arquivo 'disparos_hoje.csv' gerado.")