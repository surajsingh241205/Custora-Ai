import pandas as pd
import joblib
import os
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Load model once at startup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "churn_model.pkl")

model = joblib.load(MODEL_PATH)

def get_model_columns():
    try:
        if hasattr(model, "feature_names_in_"):
            return list(model.feature_names_in_)
        else:
            return []
    except:
        return []


def classify_risk(prob):
    if prob >= 0.7:
        return "High Risk"
    elif prob >= 0.3:
        return "Medium Risk"
    else:
        return "Low Risk"


def extract_top_features(input_df):
    try:
        if hasattr(model, "named_steps"):

            step_keys = list(model.named_steps.keys())

            logistic_model = None
            for key in step_keys:
                if "logistic" in key.lower() or "classifier" in key.lower():
                    logistic_model = model.named_steps[key]

            if logistic_model is None:
                logistic_model = list(model.named_steps.values())[-1]

            preprocessor = None
            for key in step_keys:
                if "preprocess" in key.lower():
                    preprocessor = model.named_steps[key]

            if preprocessor is not None:
                feature_names = preprocessor.get_feature_names_out()
            else:
                feature_names = input_df.columns

        else:
            logistic_model = model
            feature_names = input_df.columns

        coefficients = logistic_model.coef_[0]

        importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Coefficient": coefficients,
            "Importance": np.abs(coefficients)
        })

        importance_df = importance_df.sort_values(
            by="Importance",
            ascending=False
        ).head(5)

        return importance_df[["Feature", "Coefficient"]]

    except Exception:
        return pd.DataFrame(columns=["Feature", "Coefficient"])


def predict_churn(file):

    df = pd.read_csv(file)

    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])

    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    df.dropna(inplace=True)

    if "SeniorCitizen" in df.columns:
        df["SeniorCitizen"] = df["SeniorCitizen"].astype("object")

    if "TotalCharges" in df.columns and "tenure" in df.columns:
        df["AvgChargePerMonth"] = df["TotalCharges"] / (df["tenure"] + 1)

    # ===== STORE TRUE LABEL IF EXISTS =====
    y_true = None
    if "Churn" in df.columns:
        y_true = df["Churn"]

    # Convert Yes/No to 1/0 if needed
    if y_true.dtype == object:
        y_true = y_true.map({"Yes": 1, "No": 0})


    # ===== PREDICTION =====
    probabilities = model.predict_proba(df)[:, 1]
    predictions = model.predict(df)

    df["Churn_Probability (%)"] = (probabilities * 100).round(2)
    df["Prediction"] = predictions
    df["Risk_Level"] = [classify_risk(p) for p in probabilities]

    # ===== METRICS =====
    metrics = None

    if y_true is not None:
        metrics = {
            "accuracy": round(accuracy_score(y_true, predictions), 4),
            "precision": round(precision_score(y_true, predictions), 4),
            "recall": round(recall_score(y_true, predictions), 4),
            "f1": round(f1_score(y_true, predictions), 4),
            "conf_matrix": confusion_matrix(y_true, predictions).tolist()
        }

    top_features = extract_top_features(df)

    return df, top_features, metrics
