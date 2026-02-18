import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --- OS GLADIADORES (MODELOS) ---
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor

warnings.filterwarnings('ignore')

# ==============================================================================
# 1. GERAÇÃO DE DADOS COMPLEXOS (Varejo Realista)
# ==============================================================================
np.random.seed(42)
n_samples = 2000

print("🎲 Gerando dados de vendas de lojas físicas e e-commerce...")

data = {
    'investimento_marketing': np.random.uniform(500, 5000, n_samples), # R$ investido
    'preco_produto': np.random.uniform(50, 200, n_samples),            # Preço unitário
    'dia_semana': np.random.choice(['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom'], n_samples),
    'feriado': np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),    # É feriado?
    'temperatura_media': np.random.uniform(15, 35, n_samples),         # Clima afeta moda
    'concorrente_em_promocao': np.random.choice([0, 1], n_samples),
}

df = pd.DataFrame(data)

# --- CRIANDO O TARGET (Unidades Vendidas) COM LÓGICA DE NEGÓCIO ---
# Fórmula secreta do mercado:
# - Preço alto derruba venda.
# - Marketing sobe venda (mas tem teto).
# - Fim de semana vende mais.
# - Frio vende mais casaco (vamos supor que é coleção de inverno).

base_vendas = 100 
efeito_preco = (200 - df['preco_produto']) * 0.8  # Quanto mais barato, mais vende
efeito_mkt = np.log(df['investimento_marketing']) * 10
efeito_fds = df['dia_semana'].isin(['Sab', 'Dom']).astype(int) * 30
efeito_temp = (35 - df['temperatura_media']) * 2 # Quanto mais frio, mais vende

# Somando tudo e adicionando um erro aleatório (o caos do mundo real)
demanda_real = base_vendas + efeito_preco + efeito_mkt + efeito_fds + efeito_temp + np.random.normal(0, 15, n_samples)
df['unidades_vendidas'] = np.maximum(0, demanda_real).astype(int) # Não existe venda negativa

print(f"📊 Base pronta: {len(df)} registros. Venda Média: {df['unidades_vendidas'].mean():.0f} unidades/dia.")

# ==============================================================================
# 2. PREPARAÇÃO DO PIPELINE
# ==============================================================================
X = df.drop('unidades_vendidas', axis=1)
y = df['unidades_vendidas']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tratamento Numérico (Essencial para Redes Neurais e SVR)
numeric_features = ['investimento_marketing', 'preco_produto', 'temperatura_media']
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Tratamento Categórico
categorical_features = ['dia_semana']
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# ==============================================================================
# 3. A BATALHA DOS 7 EXÉRCITOS (GRID SEARCH)
# ==============================================================================
# Aqui definimos os competidores. Note que Regressão Polinomial é um LinearRegression com Features Polinomiais antes.

modelos = [
    {
        'nome': '1. Regressão Linear (Simples)',
        'estimator': LinearRegression(),
        'params': {} # Sem hiperparâmetros para tunar no linear simples
    },
    {
        'nome': '2. Regressão Polinomial (Curvas)',
        'estimator': Pipeline([('poly', PolynomialFeatures()), ('linear', LinearRegression())]),
        'params': {'poly__degree': [2]} # Testa polinômio de grau 2
    },
    {
        'nome': '3. Decision Tree (Árvore)',
        'estimator': DecisionTreeRegressor(random_state=42),
        'params': {'max_depth': [5, 10, None]}
    },
    {
        'nome': '4. Random Forest (Floresta)',
        'estimator': RandomForestRegressor(random_state=42),
        'params': {'n_estimators': [50, 100], 'max_depth': [10, 20]}
    },
    {
        'nome': '5. XGBoost (O Campeão do Kaggle)',
        'estimator': XGBRegressor(random_state=42),
        'params': {'n_estimators': [50, 100], 'learning_rate': [0.05, 0.1]}
    },
    {
        'nome': '6. SVR (Support Vector Regression)',
        'estimator': SVR(),
        'params': {'C': [1, 10], 'kernel': ['rbf']} # Cuidado: SVR é lento
    },
    {
        'nome': '7. MLP Neural Network (Rede Neural)',
        'estimator': MLPRegressor(random_state=42, max_iter=500),
        'params': {'hidden_layer_sizes': [(50,), (100,)], 'activation': ['relu']}
    }
]

melhor_modelo = None
melhor_score_r2 = -float('inf')
melhor_nome = ""
resultados_lista = []

print("\n🥊 INICIANDO TORNEIO DE REGRESSÃO...")
print("-" * 80)
print(f"{'MODELO':<35} | {'RMSE (Erro Médio)':<20} | {'R² (Precisão)':<10}")
print("-" * 80)

for item in modelos:
    # Pipeline individual para cada modelo (necessário pois alguns precisam de pre-processamento diferente)
    # Mas aqui usaremos o preprocessor padrão para todos para simplificar a comparação
    
    # Se for Polinomial, o estimator já é um pipeline, então tratamos diferente
    if 'Polinomial' in item['nome']:
        model_pipeline = Pipeline(steps=[('preprocessor', preprocessor), 
                                         ('poly', item['estimator'].steps[0][1]),
                                         ('linear', item['estimator'].steps[1][1])])
        # Ajuste params para o pipeline
        grid_params = {f'poly__{k.split("__")[1]}': v for k, v in item['params'].items()}
    else:
        model_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', item['estimator'])])
        grid_params = {f'regressor__{k}': v for k, v in item['params'].items()}

    grid = GridSearchCV(model_pipeline, grid_params, cv=3, scoring='neg_root_mean_squared_error', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    # Avaliando
    y_pred_grid = grid.best_estimator_.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred_grid))
    r2 = r2_score(y_test, y_pred_grid)
    
    print(f"{item['nome']:<35} | {rmse:.2f} unidades{' '*6} | {r2:.2%}")
    
    if r2 > melhor_score_r2:
        melhor_score_r2 = r2
        melhor_modelo = grid.best_estimator_
        melhor_nome = item['nome']

print("-" * 80)
print(f"🏆 GRANDE CAMPEÃO: {melhor_nome.upper()} com {melhor_score_r2:.2%} de precisão!")
print("-" * 80)

# ==============================================================================
# 4. SIMULAÇÃO FINANCEIRA (ESTOQUE)
# ==============================================================================
print("\n💰 SIMULAÇÃO DE ESTOQUE (GANHO FINANCEIRO)")
print("=" * 60)

# PREMISSAS
# Vamos comparar o Modelo vs. "Média Móvel" (O jeito antigo que as empresas fazem)
y_pred_final = melhor_modelo.predict(X_test)

# Baseline: O gerente chuta que vai vender a média do passado
previsao_gerente = np.full(len(y_test), y_train.mean()) 

# Custos
custo_oportunidade = 50.00  # Lucro que deixo de ganhar se faltar produto (Stockout)
custo_estoque = 20.00       # Custo de armazenar produto encalhado (Overstock)

def calcular_prejuizo(reais, previstos):
    prejuizo_total = 0
    for real, pred in zip(reais, previstos):
        erro = pred - real
        if erro < 0: # Previ menos do que vendeu (Faltou produto)
            prejuizo_total += abs(erro) * custo_oportunidade
        elif erro > 0: # Previ mais do que vendeu (Sobrou produto)
            prejuizo_total += abs(erro) * custo_estoque
    return prejuizo_total

perda_gerente = calcular_prejuizo(y_test, previsao_gerente)
perda_ia = calcular_prejuizo(y_test, y_pred_final)

print(f"1. ESTRATÉGIA TRADICIONAL (Média/Feeling):")
print(f"   - Prejuízo por erro de estoque: R$ {perda_gerente:,.2f}")

print(f"\n2. ESTRATÉGIA COM IA ({melhor_nome}):")
print(f"   - Prejuízo por erro de estoque: R$ {perda_ia:,.2f}")

economia = perda_gerente - perda_ia
print(f"\n🚀 DINHEIRO SALVO PELA IA: R$ {economia:,.2f}")
print(f"   (Redução de {100 - (perda_ia/perda_gerente*100):.1f}% nas perdas)")
print("=" * 60)