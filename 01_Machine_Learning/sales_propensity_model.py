import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score

# Ignorar avisos chatos do sklearn para limpar a tela
warnings.filterwarnings('ignore')

# ==============================================================================
# 1. GERAÇÃO DE DADOS (COM PADRÕES VICIADOS PARA A IA APRENDER)
# ==============================================================================
np.random.seed(42)
n_samples = 5000

print("🎲 Gerando dados simulados de navegação e compras...")

data = {
    'id_cliente': range(1, n_samples + 1),
    'visitas_site_ultimo_mes': np.random.randint(0, 30, n_samples),
    'tempo_medio_pagina_seg': np.random.randint(10, 600, n_samples), # Segundos
    'adicionou_carrinho_abandonou': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
    'dispositivo': np.random.choice(['Mobile', 'Desktop', 'Tablet'], n_samples),
    'comprou_colecao_anterior': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
}

df = pd.DataFrame(data)

# --- CRIANDO A LÓGICA DO ALVO (TARGET) ---
# Quem compra (1) geralmente tem este comportamento:
# Visita muito, fica muito tempo E já comprou antes.
score_compra = (
    (df['visitas_site_ultimo_mes'] * 0.5) + 
    (df['tempo_medio_pagina_seg'] / 60) + 
    (df['comprou_colecao_anterior'] * 10) +
    (df['adicionou_carrinho_abandonou'] * 5)
)
# Normalizando para probabilidade (Sigmoid fake)
probabilidade = 1 / (1 + np.exp(-(score_compra - score_compra.mean()) / 5))
df['comprou'] = np.random.binomial(1, probabilidade)

print(f"📊 Base pronta: {len(df)} clientes. Taxa de Conversão Real: {df['comprou'].mean():.1%}")

# ==============================================================================
# 2. PREPARAÇÃO DO PIPELINE (ENGENHARIA DE DADOS)
# ==============================================================================
X = df.drop(['id_cliente', 'comprou'], axis=1)
y = df['comprou']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tratamento Numérico
numeric_features = ['visitas_site_ultimo_mes', 'tempo_medio_pagina_seg']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Tratamento Categórico
categorical_features = ['dispositivo', 'adicionou_carrinho_abandonou', 'comprou_colecao_anterior']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# ==============================================================================
# 3. BATALHA DE MODELOS (GRID SEARCH)
# ==============================================================================
# Aqui definimos os competidores e quais "armas" (hiperparâmetros) eles podem usar.

modelos_para_testar = [
    {
        'nome': 'Logistic Regression (O Clássico)',
        'estimator': LogisticRegression(),
        'params': {
            'classifier__C': [0.1, 1.0, 10], # Força da regularização
        }
    },
    {
        'nome': 'Random Forest (A Democracia)',
        'estimator': RandomForestClassifier(random_state=42),
        'params': {
            'classifier__n_estimators': [50, 100], # Quantas árvores?
            'classifier__max_depth': [5, 10],      # Profundidade da árvore
        }
    },
    {
        'nome': 'Gradient Boosting (O Especialista)',
        'estimator': GradientBoostingClassifier(random_state=42),
        'params': {
            'classifier__learning_rate': [0.01, 0.1], # Velocidade de aprendizado
            'classifier__n_estimators': [50, 100],
        }
    }
]

melhor_modelo_global = None
melhor_score_global = 0
melhor_nome_global = ""

print("\n🥊 INICIANDO A BATALHA DE MODELOS (GRID SEARCH)...")
print("-" * 60)

for modelo_info in modelos_para_testar:
    print(f"Testando: {modelo_info['nome']}...")
    
    # Cria o Pipeline completo para este modelo
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', modelo_info['estimator'])])
    
    # O GridSearch vai testar TODAS as combinações de parâmetros acima
    grid = GridSearchCV(pipeline, modelo_info['params'], cv=3, scoring='roc_auc', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    print(f"   ✅ Melhor ROC-AUC Interno: {grid.best_score_:.4f}")
    print(f"   ⚙️ Melhores Parâmetros: {grid.best_params_}")
    
    # Verifica se este é o novo campeão
    if grid.best_score_ > melhor_score_global:
        melhor_score_global = grid.best_score_
        melhor_modelo_global = grid.best_estimator_ # Guarda o modelo treinado
        melhor_nome_global = modelo_info['nome']

print("-" * 60)
print(f"🏆 O VENCEDOR FOI: {melhor_nome_global.upper()}")
print(f"🏅 Score Final (Validação): {melhor_score_global:.4f}")
print("-" * 60)

# ==============================================================================
# 4. AVALIAÇÃO FINAL E IMPACTO FINANCEIRO
# ==============================================================================
# Usamos o MELHOR modelo para fazer as previsões finais
y_pred = melhor_modelo_global.predict(X_test)
y_proba = melhor_modelo_global.predict_proba(X_test)[:, 1]

# Métricas Técnicas
print("\n📈 RESULTADOS NO CONJUNTO DE TESTE (MUNDO REAL)")
print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
print(f"Precision (Acerto no Alvo): {precision_score(y_test, y_pred):.2f}")
print(f"Recall (Cobertura): {recall_score(y_test, y_pred):.2f}")

# ==============================================================================
# 5. SIMULAÇÃO DE CENÁRIOS DE NEGÓCIO (A VIRADA DO JOGO)
# ==============================================================================
print("\n" + "="*40)
print("💰 CÁLCULO DE ROI AVANÇADO")
print("="*40)

# --- CENÁRIO 1: O PREJUÍZO (SMS Barato - R$ 5,00) ---
# Aqui a "Pesca com Rede" (Massivo) ganha porque o custo é ínfimo.
custo_sms = 5.00
lucro_venda = 150.00

# Massivo (Manda pra todo mundo)
custo_massivo = len(y_test) * custo_sms
receita_massivo = y_test.sum() * lucro_venda
lucro_massivo = receita_massivo - custo_massivo

# IA (Manda só pra quem tem > 50% de chance)
mask_ia = y_proba > 0.5
custo_ia = mask_ia.sum() * custo_sms
receita_ia = y_test[mask_ia].sum() * lucro_venda
lucro_ia = receita_ia - custo_ia

print(f"CENÁRIO 1 (SMS Barato R$ 5,00):")
print(f"   - Lucro Massivo: R$ {lucro_massivo:,.2f}")
print(f"   - Lucro IA:      R$ {lucro_ia:,.2f}")
print(f"   🔻 Resultado: A IA perdeu porque o custo de errar (perder venda) é maior que o custo de ligar.")

# --- CENÁRIO 2: O LUCRO (Catálogo de Luxo - R$ 50,00) ---
# Aqui a IA brilha. Mandar catálogo caro pra quem não compra é suicídio financeiro.
print("\n" + "-"*40)
custo_catalogo = 50.00

# Massivo (Manda catálogo caro pra todo mundo)
custo_massivo_caro = len(y_test) * custo_catalogo
lucro_massivo_caro = receita_massivo - custo_massivo_caro

# IA (Manda catálogo caro só pra quem tem > 50%)
custo_ia_caro = mask_ia.sum() * custo_catalogo
lucro_ia_caro = receita_ia - custo_ia_caro

print(f"CENÁRIO 2 (Marketing de Luxo R$ 50,00):")
print(f"   - Lucro Massivo: R$ {lucro_massivo_caro:,.2f} (Prejuízo ou lucro baixo)")
print(f"   - Lucro IA:      R$ {lucro_ia_caro:,.2f} (Eficiência Máxima)")
print(f"\n🚀 DIFERENÇA (O QUE A IA SALVOU): R$ {lucro_ia_caro - lucro_massivo_caro:,.2f}")
print("="*40)