from django.apps import AppConfig
import os, joblib
class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'
    def ready(self):
        # load model into ml module if available
        try:
            from . import ml
            model_path = os.getenv('MODEL_PATH')
            if model_path and os.path.exists(model_path):
                ml.model = joblib.load(model_path)
            else:
                ml.model = None
        except Exception:
            pass
