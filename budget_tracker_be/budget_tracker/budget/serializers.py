from rest_framework import serializers
from .models import Transaction, Budget


class TransactionSerializer(serializers.ModelSerializer):
    """
        Serializer for the Transaction model.
        
        Includes all relevant fields of a transaction and a read-only display field for category name.
        Also includes the user field in read-only mode to track which user owns the transaction.
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'category', 'category_display', 'description', 'date']

class BudgetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Budget model.

    Provides serialization and deserialization for budget-related data including
    user, amount, month, and year fields.
    """
    class Meta:
        model = Budget
        fields = ['id', 'user', 'amount', 'month', 'year']

