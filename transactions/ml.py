# transactions/ml.py

model = None
scaler = None
feature_order = None

def predict(features: dict) -> float:
    """
    Predict fraud probability using loaded ML artifacts
    """
    global model, scaler, feature_order

    if model is None:
        raise RuntimeError("ML model not loaded")

    import numpy as np

    # Ensure consistent feature order
    if feature_order:
        X = np.array([[features[f] for f in feature_order]])
    else:
        X = np.array([list(features.values())])

    # Apply scaler if present
    if scaler is not None:
        X = scaler.transform(X)

    # Predict probability
    if hasattr(model, "predict_proba"):
        return float(model.predict_proba(X)[:, 1][0])

    # Fallback (rare)
    return float(model.predict(X)[0])