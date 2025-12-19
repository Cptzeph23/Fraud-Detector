from rest_framework import serializers, viewsets, routers
from .models import Transaction, FraudAlert

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id','phone_number','amount','merchant_id','fraud_probability','status','mpesa_checkout_request_id','created_at','updated_at','features_json']

class FraudAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudAlert
        fields = ['id','transaction','message','sent','created_at']

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.order_by('-created_at')
    serializer_class = TransactionSerializer

class FraudAlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FraudAlert.objects.order_by('-created_at')
    serializer_class = FraudAlertSerializer

router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='api-transactions')
router.register(r'alerts', FraudAlertViewSet, basename='api-alerts')