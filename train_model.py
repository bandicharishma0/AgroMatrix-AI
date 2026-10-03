import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

np.random.seed(42)

data = {
    "land_size": np.random.randint(1, 20, 300),
    "annual_income": np.random.randint(50000, 1000000, 300),
    "existing_loan": np.random.randint(0, 500000, 300),
    "repayment_history": np.random.randint(0, 11, 300),
    "crop_success": np.random.randint(0, 11, 300),
    "weather_risk": np.random.randint(0, 11, 300),
}

df = pd.DataFrame(data)

df["approved"] = (
    (df["annual_income"] > 250000) &
    (df["repayment_history"] >= 5) &
    (df["crop_success"] >= 5) &
    (df["existing_loan"] < 300000) &
    (df["weather_risk"] <= 7)
).astype(int)

X = df.drop("approved", axis=1)
y = df["approved"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

joblib.dump(model, "loan_model.pkl")

print("Model trained successfully!")
print("Accuracy:", model.score(X_test, y_test))