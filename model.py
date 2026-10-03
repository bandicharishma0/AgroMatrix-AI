import joblib
import numpy as np

model = joblib.load("loan_model.pkl")


def predict_credit(
    land_size,
    annual_income,
    existing_loan,
    repayment_history,
    crop_success,
    weather_risk
):

    data = np.array([[
        land_size,
        annual_income,
        existing_loan,
        repayment_history,
        crop_success,
        weather_risk
    ]])

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    credit_score = int(300 + probability * 600)

    if credit_score >= 750:
        risk = "Low Risk"
    elif credit_score >= 600:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    return prediction, credit_score, risk