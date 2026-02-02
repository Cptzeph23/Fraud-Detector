from django.urls import path, include
from . import views
from .api import router as api_router

urlpatterns = [
    path('', views.index, name='index'),

    # HTML flow
    path('submit/', views.transaction_form, name='transaction_form'),
    path('process/', views.create_transaction, name='create_transaction'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('alerts/', views.alerts, name='alerts'),
    path('<int:tx_id>/', views.transaction_detail, name='transaction_detail'),

    # APIs
    path('daraja/callback/', views.daraja_callback, name='daraja_callback'),
    path('api/', include(api_router.urls)),
]
