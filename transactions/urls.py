from django.urls import path, include
from . import views
from .api import router as api_router
urlpatterns = [
    path('create/', views.create_transaction, name='create_transaction'),
    path('daraja/callback/', views.daraja_callback, name='daraja_callback'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit/', views.transaction_form, name='transaction_form'),
    path('alerts/', views.alerts, name='alerts'),
    path('<int:tx_id>/', views.transaction_detail, name='transaction_detail'),
    path('api/', include(api_router.urls)),
]
