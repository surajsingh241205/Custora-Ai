import pandas as pd
import joblib
import os
import numpy as np

# Load model once at startup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "churn_model.pkl")

model = joblib.load(MODEL_PATH)


def classify_risk(prob):
    """
    Convert probability (0-1) into business risk level
    """
    if prob >= 0.7:
        return "High Risk"
    elif prob >= 0.3:
        return "Medium Risk"
    else:
        return "Low Risk"


def extract_top_features(input_df):
    """
    Extract top 5 features from Logistic Regression model
    (handles both pipeline and non-pipeline cases)
    """

    try:
        # CASE 1: If model is a Pipeline
        if hasattr(model, "named_steps"):

            # Try common step names
            step_keys = list(model.named_steps.keys())

            # Find logistic regression step automatically
            logistic_model = None
            for key in step_keys:
                if "logistic" in key.lower() or "classifier" in key.lower():
                    logistic_model = model.named_steps[key]

            # If not found, assume last step is classifier
            if logistic_model is None:
                logistic_model = list(model.named_steps.values())[-1]

            # Try to get preprocessor
            preprocessor = None
            for key in step_keys:
                if "preprocess" in key.lower():
                    preprocessor = model.named_steps[key]

            # Get transformed feature names
            if preprocessor is not None:
                feature_names = preprocessor.get_feature_names_out()
            else:
                feature_names = input_df.columns

        else:
            # CASE 2: Model is plain LogisticRegression
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
        # Fail-safe: return empty dataframe if anything breaks
        return pd.DataFrame(columns=["Feature", "Coefficient"])


def predict_churn(file):
    """
    Takes CSV file path, applies preprocessing
    used during training, and returns:
    - result dataframe
    - top 5 feature importance dataframe
    """

    # Load data
    df = pd.read_csv(file)

    # Drop customerID if present
    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])

    # Convert TotalCharges to numeric
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(
            df["TotalCharges"], errors="coerce"
        )

    # Drop missing
    df.dropna(inplace=True)

    # Convert SeniorCitizen to categorical
    if "SeniorCitizen" in df.columns:
        df["SeniorCitizen"] = df["SeniorCitizen"].astype("object")

    # Feature engineering (must match training)
    if "TotalCharges" in df.columns and "tenure" in df.columns:
        df["AvgChargePerMonth"] = df["TotalCharges"] / (df["tenure"] + 1)

    # ===== PREDICTIONS =====
    probabilities = model.predict_proba(df)[:, 1]
    predictions = model.predict(df)

    df["Churn_Probability (%)"] = (probabilities * 100).round(2)
    df["Prediction"] = predictions
    df["Risk_Level"] = [classify_risk(p) for p in probabilities]

    # ===== FEATURE IMPORTANCE =====
    top_features = extract_top_features(df)

    return df, top_features
