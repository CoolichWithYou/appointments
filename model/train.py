import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

df = pd.read_csv('symptoms.csv')

X = df['symptoms']
y = df['specialist']

from sklearn.pipeline import make_pipeline

model = make_pipeline(
    TfidfVectorizer(),
    LogisticRegression()
)

model.fit(X, y)

joblib.dump(model, 'doctor_model.pkl')