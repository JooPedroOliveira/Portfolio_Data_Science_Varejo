import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score

# ==============================================================================
# 1. GERAÇÃO DE DADOS "BIG DATA" (SIMULADO)
# ==============================================================================
# Simulando 10.000 clientes com comportamentos complexos de varejo
np.random.seed(42)
n_samples = 10000

data = {
    'id_cliente': range(1, n_samples + 1),
    'idade': np.random.randint(18, 70, n_samples),
    'tempo_como_cliente_meses': np.random.randint(1, 120, n_samples),
    'total_gasto_ultimo_ano': np.random.exponential(1500, n_samples), # R$
    'frequencia_compras_ano': np.random.randint(1, 50, n_samples),
    'categoria_favorita': np.random.choice(['Moda', 'Casa', 'Pet', 'Tech'], n_samples),
    'usou_sac_recente': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
}

df = pd.DataFrame(data)

churn_simulado = np.zeros(n_samples) # Todo mundo começa fiel (0)

# Se usou SAC, vira 1 (sai)
churn_simulado[df['usou_sac_recente'] == 1] = 1 

# Se gasta pouco, vira 1 (sai)
indices_baixo_gasto = df[df['total_gasto_ultimo_ano'] < 500].index
churn_simulado[np.random.choice(indices_baixo_gasto, size=int(len(indices_baixo_gasto)*0.5))] = 1

df['churn'] = churn_simulado.astype(int)

# Introduzindo "Sujeira" Real (Valores Nulos) para testar o Pipeline
df.loc[df.sample(500).index, 'idade'] = np.nan
df.loc[df.sample(200).index, 'categoria_favorita'] = np.nan

print(f"📊 Base carregada: {df.shape[0]} clientes. Taxa de Churn: {df['churn'].mean():.1%}")

# ==============================================================================
# 2. ENGENHARIA DE FEATURES (PROFISSIONAL)
# ==============================================================================
# Separar Features (X) e Target (y)
X = df.drop(['id_cliente', 'churn'], axis=1)
y = df['churn']

# Dividir Treino e Teste (Padrão Ouro: 80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# --- DEFINIÇÃO DO PIPELINE DE PRÉ-PROCESSAMENTO ---
# Nada de tratar dados manualmente! O Pipeline garante que o que fizermos no treino
# será aplicado IGUAL na produção.

# Tratamento para Variáveis Numéricas (Idade, Gastos)
# 1. Preenche nulos com a Mediana (SimpleImputer)
# 2. Coloca na mesma escala (StandardScaler)
numeric_features = ['idade', 'tempo_como_cliente_meses', 'total_gasto_ultimo_ano', 'frequencia_compras_ano']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Tratamento para Variáveis Categóricas (Categoria, SAC)
# 1. Preenche nulos com "Constant"
# 2. Transforma texto em números (OneHotEncoder)
categorical_features = ['categoria_favorita', 'usou_sac_recente']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Juntando tudo no Pré-Processador
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# ==============================================================================
# 3. O MODELO (XGBOOST - O REI DO VAREJO)
# ==============================================================================
# Pipeline Final: Pré-processamento -> Modelo
# scale_pos_weight ajuda a balancear (já que temos poucos cancelamentos)
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(n_estimators=100, learning_rate=0.1, scale_pos_weight=5, random_state=42))
])

print("\n⚙️ Treinando o Motor de IA (Pipeline Completo)...")
model_pipeline.fit(X_train, y_train)
print("✅ Treinamento Concluído!")

# ==============================================================================
# 4. AVALIAÇÃO DE NEGÓCIO (E NÃO SÓ ACURÁCIA)
# ==============================================================================
print("\n" + "="*40)
print("📈 RESULTADOS DO MODELO")
print("="*40)

# Previsões
y_pred = model_pipeline.predict(X_test)
y_proba = model_pipeline.predict_proba(X_test)[:, 1]

# Métricas Técnicas
print(f"ROC-AUC Score (Capacidade de Separação): {roc_auc_score(y_test, y_proba):.4f}")
print("\nRelatório de Classificação:\n", classification_report(y_test, y_pred))

# ==============================================================================
# 5. APLICAÇÃO PRÁTICA (SIMULAÇÃO DE PRODUÇÃO)
# ==============================================================================
print("\n" + "="*40)
print("💰 IMPACTO NO NEGÓCIO (SIMULAÇÃO)")
print("="*40)

# Pegamos os clientes do teste e simulamos uma ação de marketing
results = X_test.copy()
results['Risco_Churn_Prob'] = y_proba
results['Real_Churn'] = y_test

# Regra de Negócio: Se a probabilidade de sair for > 70%, é "Alto Risco"
alto_risco = results[results['Risco_Churn_Prob'] > 0.7]
dinheiro_em_risco = alto_risco['total_gasto_ultimo_ano'].sum()

print(f"🚨 Clientes em Zona de Risco (>70%): {len(alto_risco)}")
print(f"💸 Receita Anual em Perigo (LTV em Risco): R$ {dinheiro_em_risco:,.2f}")
print("📢 Ação Sugerida: Enviar cupom de 10% ou ligar para estes clientes HOJE.")