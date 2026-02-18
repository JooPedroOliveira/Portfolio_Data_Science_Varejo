# 🛍️ Portfólio de Data Science & AI Engineering - Varejo

Bem-vindo ao meu portfólio de engenharia.
Aqui consolido soluções práticas de **Machine Learning**, **Engenharia de Dados** e **IA Generativa (LLMs)** aplicadas a problemas reais do varejo de moda, focando em eficiência operacional, aumento de receita e automação inteligente.
---

## 🧠 1. Machine Learning & Análise Preditiva
*Modelos matemáticos para tomada de decisão estratégica.*

| Projeto | Arquivo | Descrição de Negócio |
| :--- | :--- | :--- |
| **Previsão de Churn** | `churn_prediction_xgboost.py` | Modelo XGBoost para identificar clientes em risco de cancelamento, permitindo ações de retenção proativas. |
| **Previsão de Demanda** | `demand_forecasting_regressao.py` | Algoritmo de Regressão Polinomial para prever vendas futuras e otimizar níveis de estoque (evitando ruptura/encalhe). |
| **Clusterização de Clientes** | `customer_segmentation_kmeans.py` | Segmentação não-supervisionada (K-Means) baseada em RFM (Recência, Frequência, Valor) para campanhas de marketing personalizadas. |
| **Propensão de Vendas** | `sales_propensity_model.py` | Cálculo de probabilidade de compra para priorizar leads quentes (Lead Scoring). |
---

## 🤖 2. Agentes de IA Generativa & RAG (LLMs)
*Automação inteligente usando Google Gemini, OpenAI e LangChain.*

### 📚 RAG (Retrieval-Augmented Generation)
* **Chatbot de Vendas (PDF):** (`sales_assistant_app.py`, `rag_knowledge_base_core.py`)
    * Assistente que lê manuais internos e responde dúvidas de vendedores em tempo real sobre políticas de troca e descontos.
* **Analista de CSV:** (`structured_data_rag.py`)
    * Agente capaz de "conversar" com planilhas de Excel/CSV para extrair insights sem precisar de SQL.
* **Motor de Busca Semântica:** (`semantic_search_engine.py`, `vector_db_setup.py`)
    * Sistema de busca vetorial que entende o significado (Ex: "Roupa de baixo" encontra "Calcinha") usando ChromaDB.

### 💼 Agentes Especialistas
* **Agente de Recuperação:** (`sales_recovery_agent.py`)
    * Robô focado em re-engajar clientes que abandonaram carrinhos ou pararam de comprar.
* **Consultor de BI:** (`bi_consultant_agent.py`)
    * Agente estratégico que analisa KPIs e sugere ações de negócio.
* **Analista SQL:** (`sql_analyst.py`)
    * IA que traduz perguntas em português ("Quantas vendas ontem?") para código SQL executável.
* **Agente Logístico:** (`logistics_ai_agent.py`)
    * Otimização de rotas e rastreio inteligente.

---

## 👁️ 3. Visão Computacional & Multimodal
*Transformando imagens e áudio em dados estruturados.*

* **Busca Visual de Produtos:** (`product_visual_search.py`)
    * Sistema que permite encontrar produtos similares enviando apenas uma foto.
* **OCR de Notas Fiscais:** (`image_to_data_ocr.py`)
    * Extração automática de dados de fotos de cupons e documentos para o ERP.
* **Auditor de Áudio (Call Center):** (`call_center_audio_auditor.py`)
    * Transcrição e análise automática de ligações do SAC para controle de qualidade.
* **Análise de Gráficos Financeiros:** (`financial_chart_analyzer.py`)
    * IA que "olha" para imagens de gráficos e explica a tendência de alta/baixa.

---

## 📊 4. Engenharia de Dados & Analytics
*Infraestrutura e monitoramento.*

* **Pipeline ETL:** (`etl_data_pipeline.py`)
    * Automação da extração, transformação e carga de dados brutos.
* **Análise de Sentimento (NPS):** (`nps_sentiment_analysis.py`)
    * Classificação automática de comentários de clientes (Positivo/Negativo) para cálculo de NPS.
---

## 🛠️ Stack Tecnológico
* **Linguagens:** Python 3.10+
* **Machine Learning:** Scikit-Learn, XGBoost, Pandas, NumPy.
* **GenAI / LLMs:** LangChain, Google Gemini API, OpenAI API, ChromaDB (Vetor).
* **Visão/Áudio:** Tesseract OCR, Speech Recognition.
* **Ambiente:** Git, VS Code/Cursor.

---
*Desenvolvido por João Pedro Alencar Dores de Oliveira - Engenheiro de IA e Machine Learning & Supervisor de BI.*