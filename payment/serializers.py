# payment/serializers.py

from rest_framework import serializers
from .models import Payment, PaymentItem

class PaymentItemSerializer(serializers.ModelSerializer):
    tour_title = serializers.CharField(source='tour.title', read_only=True)

    class Meta:
        model = PaymentItem
        fields = ['id', 'tour', 'tour_title', 'amount']


class PaymentSerializer(serializers.ModelSerializer):
    items = PaymentItemSerializer(source='paymentitem_set', many=True, read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'is_paid', 'payment_date', 'items']
        read_only_fields = ['user', 'is_paid', 'payment_date']
