from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    order_total = serializers.DecimalField(source='order.total_price', max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'order_total', 'amount', 'method', 'status', 'transaction_id', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
        
class InitiatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    method = serializers.ChoiceField(choices=['card', 'upi', 'cod', 'wallet'])
            