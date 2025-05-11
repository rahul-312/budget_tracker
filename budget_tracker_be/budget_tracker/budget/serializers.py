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

class SaveSavingsSerializer(serializers.Serializer):
    """
    Serializer for saving leftover savings data to be carried forward to the next month.

    Fields:
    - savings: The amount of savings to be carried forward (non-negative).
    - next_month: The month (1-12) for which the savings should be applied.
    - next_year: The year (>= current year) for which the savings should be applied.
    """
    savings = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.00)
    next_month = serializers.IntegerField(min_value=1, max_value=12)
    next_year = serializers.IntegerField(min_value=2023)