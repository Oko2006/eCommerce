from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'order',
            'provider',
            'status',
            'transaction_id',
            'amount',
            'currency',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['status', 'amount', 'created_at', 'updated_at']
