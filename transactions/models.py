from django.db import models
from django.contrib.auth.models import User
class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('SUCCESS','Success'),
        ('FAILED','Failed'),
        ('FLAGGED','Flagged'),
    ]
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    merchant_id = models.CharField(max_length=100, blank=True, null=True)
    features_json = models.JSONField(null=True, blank=True)
    fraud_probability = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    mpesa_checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"TX-{self.id} {self.phone_number} {self.amount}"
class FraudAlert(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='alerts')
    message = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Alert for {self.transaction.id}"
