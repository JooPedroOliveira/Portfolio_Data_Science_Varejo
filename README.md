# 🛍️ Portfólio de Data Science & AI Engineering - Varejo

Bem-vindo ao meu portfólio de engenharia.
Aqui consolido soluções práticas de **Machine Learning**, **Engenharia de Dados** e **IA Generativa (LLMs)** aplicadas a problemas reais do varejo de moda e E-commerce, focando em eficiência operacional, aumento de receita e automação inteligente.

---

## 👨‍💻 Sobre Mim
**João Pedro Alencar Dores Oliveira**
*Supervisor de BI & Engenheiro de IA e Machine Learning*

Engenheiro Civil (Mackenzie) transicionado para a área de Dados e Tecnologia. Atualmente Supervisor de Business Intelligence na C&A, liderando estratégias de dados para o varejo de moda.
Minha carreira combina a visão analítica da engenharia com a inovação da Inteligência Artificial. Especialista em transformar dados brutos em decisões executivas, hoje foco no desenvolvimento de **Agentes de IA** e **Sistemas Preditivos** para otimizar vendas e operações.
[Conecte-se comigo no LinkedIn](https://www.linkedin.com/in/joão-pedro-alencar-dores-oliveira)

---

## 🧠 1. Machine Learning & Análise Preditiva
*Algoritmos matemáticos para tomada de decisão estratégica.*

| Projeto | Arquivo | Descrição Técnica & Negócio |
| :--- | :--- | :--- |
| **Previsão de Churn** | `churn_prediction_xgboost.py` | Modelo **XGBoost Classifier** otimizado para identificar clientes com alto risco de cancelamento. Foco em maximizar o Recall para retenção. |
| **Previsão de Demanda** | `demand_forecasting_regressao.py` | Comparativo entre **Regressão Linear, Polinomial e Redes Neurais** para prever vendas futuras e evitar ruptura de estoque. |
| **Clusterização (CRM)** | `customer_segmentation_kmeans.py` | Algoritmo **K-Means** aplicado sobre matriz RFM (Recência, Frequência, Valor) para segmentar base em clusters (Vip, Hibernando, Churn). |
| **Propensão de Vendas** | `sales_propensity_model.py` | Modelo de **Logistic Regression** para Lead Scoring (probabilidade de compra). |

---

## 🤖 2. Agentes de IA Generativa & RAG (LLMs)
*Automação inteligente usando Google Gemini, OpenAI e LangChain.*

### 🛍️ Experiência do Cliente & Marketing (Front-Office)
* **CRM de Hiper-Personalização:** (`projeto_crm_pet.py`)
    * **O que faz:** Sistema Híbrido (Pandas + LLM). Analisa a recência de compra do cliente (RFM) e usa IA Generativa para criar mensagens de WhatsApp **únicas para cada cliente**, citando o nome e o produto favorito para recuperar vendas (Churn).
* **Personal Stylist IA:** (`sales_assistant_app.py`)
    * **O que faz:** Assistente de vendas que usa **Busca Semântica (Vector Search)** no estoque. O cliente diz *"Quero um look para casamento na praia"* e a IA busca produtos visualmente similares e argumenta a venda.
* **Agente de Recuperação:** (`sales_recovery_agent.py`)
    * **O que faz:** Robô focado em carrinho abandonado. Gera mensagens persuasivas baseadas em gatilhos mentais de escassez.

### ⚙️ Eficiência Operacional (Back-Office)
* **Chatbot de Manuais (RAG):** (`rag_knowledge_base_core.py` / `structured_data_rag.py`)
    * **O que faz:** Sistema que lê PDFs de normas internas e tira dúvidas de funcionários sobre regras de negócio.
* **Analista SQL Autônomo:** (`sql_analyst.py`)
    * **O que faz:** Agente Text-to-SQL. Traduz perguntas de diretores em português ("Qual foi a venda de Jeans ontem?") diretamente em código SQL executável.
* **Consultor de BI:** (`bi_consultant_agent.py`)
    * **O que faz:** Analisa tabelas de KPIs e gera relatórios executivos textuais apontando ofensores e oportunidades.

---

## 👁️ 3. Visão Computacional & Multimodal
*Transformando imagens e áudio em dados estruturados.*

* **Busca Visual de Produtos:** (`product_visual_search.py`)
    * Sistema que permite encontrar produtos similares enviando apenas uma foto de referência.
* **OCR de Notas Fiscais:** (`image_to_data_ocr.py`)
    * Extração automática de dados de fotos de cupons fiscais para conciliação no ERP.
* **Auditor de Áudio (SAC):** (`call_center_audio_auditor.py`)
    * Transcrição e análise de sentimento de ligações do Call Center para controle de qualidade.

---

## 🛠️ Stack Tecnológico Detalhado

### Machine Learning & Estatística
* **Algoritmos:** Linear/Polynomial Regression, XGBoost, Random Forest, K-Means Clustering, Neural Networks (MLP), Logistic Regression.
* **Bibliotecas:** Scikit-Learn, Statsmodels, NumPy, Pandas.

### Inteligência Artificial (GenAI)
* **LLMs:** Google Gemini 2.5 Flash/Pro, OpenAI GPT, Perplexity, Cloud, Grok.
* **Orquestração:** LangChain, LangGraph.
* **Vector Database:** ChromaDB (Busca Semântica e Embeddings).
* **Engenharia de Prompt:** Few-Shot Prompting, Chain-of-Thought, Contextual Grounding.

### Engenharia de Dados
* **Ferramentas:** Python (ETL), SQL, Power BI, Excel, Git/GitHub.

---
*Desenvolvido por João Pedro Alencar - [Conecte-se comigo no LinkedIn](https://www.linkedin.com/in/joão-pedro-alencar-dores-oliveira)*