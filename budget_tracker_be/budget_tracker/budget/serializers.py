from rest_framework import serializers
from .models import Transaction, Budget


class TransactionSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'category', 'category_display', 'description', 'date']

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'user', 'amount', 'month', 'year']

class SaveSavingsSerializer(serializers.Serializer):
    savings = serializers.DecimalField(max_digits=10, decimal_places=2)
    next_month = serializers.IntegerField()
    next_year = serializers.IntegerField()