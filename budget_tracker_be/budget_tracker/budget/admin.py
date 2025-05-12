from django.contrib import admin
from .models import Transaction, Budget

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'date')
    list_filter = ('category', 'date')
    search_fields = ('user__username', 'description', 'category')
    ordering = ('-date',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'spent_amount', 'month', 'year')
    list_filter = ('month', 'year')
    search_fields = ('user__username',)
    ordering = ('-year', '-month')
