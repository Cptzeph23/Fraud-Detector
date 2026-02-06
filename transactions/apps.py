# transactions/apps.py

from django.apps import AppConfig
import os, joblib

class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'

    def ready(self):
        from . import ml
        from django.conf import settings
        import os

        model_path = os.getenv("MODEL_PATH")
        
        if model_path and not os.path.isabs(model_path):
             model_path = os.path.join(settings.BASE_DIR, model_path)

        if not model_path or not os.path.exists(model_path):
            print("❌ MODEL_PATH invalid or missing")
            ml.model = None
            return

        try:
            obj = joblib.load(model_path)

            # Handle dict-based artifacts
            if isinstance(obj, dict):
                ml.model = obj.get("model")
                ml.scaler = obj.get("scaler")
                ml.feature_order = obj.get("features")
            else:
                ml.model = obj
                ml.scaler = None
                ml.feature_order = None

            print("✅ ML model, scaler & features loaded")

        except Exception as e:
            print("❌ Failed to load ML model:", e)
            ml.model = None