from django.urls import path
from . import views
urlpatterns = [
    path('create/', views.create_transaction, name='create_transaction'),
    path('daraja/callback/', views.daraja_callback, name='daraja_callback'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit/', views.transaction_form, name='transaction_form'),
    path('alerts/', views.alerts, name='alerts'),
]
