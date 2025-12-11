# ML helper module - model is loaded by app config
model = None
def predict(features):
    if model is None:
        raise RuntimeError('Model not loaded. Place your .pkl and set MODEL_PATH')
    import numpy as np
    # features: dict -> maintain order consistent with training
    if isinstance(features, dict):
        X = np.array([list(features.values())])
    else:
        X = np.array(features)
    prob = model.predict_proba(X)[:,1][0]
    return float(prob)
