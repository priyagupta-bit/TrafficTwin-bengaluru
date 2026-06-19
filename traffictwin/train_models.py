import pandas as pd
import numpy as np

df = pd.read_csv('data/raw/train.csv')

print(df.shape)
df.head(5)

print(df.info())

print("\nMissing Values:")
print(df.isnull().sum().sort_values(ascending=False))


df['start_datetime'] = pd.to_datetime(df['start_datetime'],errors='coerce')

df['hour'] = df['start_datetime'].dt.hour
df['weekday'] = df['start_datetime'].dt.dayofweek
df['month'] = df['start_datetime'].dt.month

df['priority_target'] = (df['priority'] == 'High').astype(int)

df['closure_target'] = (df['requires_road_closure']).astype(int)

features = ['event_type','event_cause','zone','junction','veh_type','hour','weekday','month']

model_df = df[features +['priority_target', 'closure_target']].copy()

for col in ['event_type','event_cause','zone','junction','veh_type']:
    model_df[col] = model_df[col].fillna('Unknown')

for col in ['hour','weekday','month']:
    model_df[col] = model_df[col].fillna(-1)

print(model_df.shape)
model_df.head()

from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

X = model_df.drop(['priority_target','closure_target'],axis=1)

y = model_df['priority_target']

cat_features = ['event_type','event_cause','zone','junction','veh_type']

X_train, X_test, y_train, y_test = train_test_split(
    X,y,test_size=0.2,random_state=42,stratify=y
)

priority_model = CatBoostClassifier(
    iterations=1000,
    depth=6,
    learning_rate=0.05,
    loss_function='Logloss',
    eval_metric='AUC',
    random_seed=42,
    verbose=False
)

priority_model.fit(
    X_train,
    y_train,
    cat_features=cat_features
)

priority_pred = priority_model.predict_proba(X_test)[:,1]

print(
    "Priority AUC:",
    roc_auc_score(y_test, priority_pred)
)

X = model_df.drop(['priority_target','closure_target'],axis=1)

y = model_df['closure_target']

X_train, X_test, y_train, y_test = train_test_split(
    X,y,test_size=0.2,random_state=42,stratify=y
)

closure_model = CatBoostClassifier(
    iterations=1000,
    depth=6,
    learning_rate=0.05,
    auto_class_weights='Balanced',
    eval_metric='AUC',
    random_seed=42,
    verbose=False
)

closure_model.fit(
    X_train,
    y_train,
    cat_features=cat_features
)

closure_pred = closure_model.predict_proba(X_test)[:,1]

print("Closure AUC:",roc_auc_score(y_test, closure_pred))

import joblib

joblib.dump(priority_model,"models/priority_model.pkl")

joblib.dump(closure_model,"models/closure_model.pkl")

print("Models saved")

risk_df = (
    df.groupby('junction')
      .agg(
          incidents=('id','count'),
          high_priority_rate=('priority_target','mean'),
          closure_rate=('closure_target','mean')
      )
)

risk_df = risk_df[risk_df['incidents'] >= 20]

risk_df['risk_score'] = (0.5 * risk_df['high_priority_rate']+ 0.3 * risk_df['closure_rate']
    + 0.2 * (risk_df['incidents']/ risk_df['incidents'].max()))

risk_df = risk_df.sort_values('risk_score',ascending=False)

risk_df.to_csv("data/processed/risk_index.csv")

print(risk_df.head(20))