from django.contrib import admin
from .models import Transaction, FraudAlert
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','phone_number','amount','status','fraud_probability','created_at')
    list_filter = ('status',)
    search_fields = ('phone_number','mpesa_checkout_request_id')
@admin.register(FraudAlert)
class FraudAlertAdmin(admin.ModelAdmin):
    list_display = ('transaction','sent','created_at')
