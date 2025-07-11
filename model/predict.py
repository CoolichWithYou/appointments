import joblib

model = joblib.load('doctor_model.pkl')

symptoms = "болит живот и тошнит"
specialist = model.predict([symptoms])[0]

print("Вам нужен врач:", specialist)