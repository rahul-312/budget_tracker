from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction, Budget
from .serializers import TransactionSerializer, BudgetSerializer
from rest_framework.exceptions import NotFound
from datetime import datetime
from .models import CategoryType
from collections import defaultdict
from decimal import Decimal
from django.db.models.functions import TruncMonth
from django.db.models import Sum

class CategoryChoicesView(APIView):
    """
    API view to retrieve the available transaction categories.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Returns a list of available categories for transactions.
        """
        choices = [
            {"value": choice[0], "label": choice[1]}
            for choice in CategoryType.choices
        ]
        return Response(choices)

class TransactionView(APIView):
    """
    API view for managing transactions.
    Allows for creating, retrieving, updating, and deleting transactions.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id=None, *args, **kwargs):
        """
        Retrieves a specific transaction or all transactions for the authenticated user.
        """
        if transaction_id:
            try:
                transaction = Transaction.objects.get(id=transaction_id, user=request.user)
                serializer = TransactionSerializer(transaction)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Transaction.DoesNotExist:
                raise NotFound(detail="Transaction not found.")
        else:
            transactions = Transaction.objects.filter(user=request.user)
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Creates a new transaction and updates the associated budget for the current month.
        """
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(user=request.user)

            today = datetime.today()
            current_month = today.month
            current_year = today.year

            try:
                budget = Budget.objects.get(user=request.user, month=current_month, year=current_year)
            except Budget.DoesNotExist:
                return Response({"detail": "No budget found for the current month."}, status=status.HTTP_404_NOT_FOUND)

            budget.spent_amount += transaction.amount
            budget.save()

            return Response({
                "transaction": serializer.data,
                "spent_amount": round(budget.spent_amount, 2),
                "remaining_budget": round(budget.amount - budget.spent_amount, 2)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, transaction_id, *args, **kwargs):
        """
        Updates an existing transaction and adjusts the associated budget.
        """
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
            today = datetime.today()
            current_month = today.month
            current_year = today.year
            budget = Budget.objects.get(user=request.user, month=current_month, year=current_year)

            # Roll back old amount
            budget.spent_amount -= transaction.amount

            serializer = TransactionSerializer(transaction, data=request.data, partial=True)
            if serializer.is_valid():
                updated_transaction = serializer.save()
                # Add new amount
                budget.spent_amount += updated_transaction.amount
                budget.save()

                return Response({
                    "transaction": serializer.data,
                    "spent_amount": round(budget.spent_amount, 2),
                    "remaining_budget": round(budget.amount - budget.spent_amount, 2)
                }, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Transaction.DoesNotExist:
            raise NotFound(detail="Transaction not found.")
        except Budget.DoesNotExist:
            return Response({"detail": "No budget found for the current month."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, transaction_id, *args, **kwargs):
        """
        Deletes a specific transaction and adjusts the associated budget.
        """
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
            today = datetime.today()
            current_month = today.month
            current_year = today.year
            budget = Budget.objects.get(user=request.user, month=current_month, year=current_year)

            budget.spent_amount -= transaction.amount
            budget.save()

            transaction.delete()
            return Response({
                "detail": "Transaction deleted successfully.",
                "spent_amount": round(budget.spent_amount, 2),
                "remaining_budget": round(budget.amount - budget.spent_amount, 2)
            }, status=status.HTTP_204_NO_CONTENT)

        except Transaction.DoesNotExist:
            raise NotFound(detail="Transaction not found.")
        except Budget.DoesNotExist:
            return Response({"detail": "No budget found for the current month."}, status=status.HTTP_404_NOT_FOUND)

class BudgetView(APIView):
    """
    API view for managing budgets.
    Allows for creating, retrieving, updating, and deleting budgets.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, budget_id=None, *args, **kwargs):
        """
        Retrieves a specific budget or all budgets for the authenticated user.
        """
        if budget_id:
            try:
                budget = Budget.objects.get(id=budget_id, user=request.user)
                serializer = BudgetSerializer(budget)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Budget.DoesNotExist:
                raise NotFound(detail="Budget not found.")
        else:
            budgets = Budget.objects.filter(user=request.user)
            serializer = BudgetSerializer(budgets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Creates a new budget for a specific month and year.
        """
        month = request.data.get('month')
        year = request.data.get('year')
        amount = request.data.get('amount')

        existing_budget = Budget.objects.filter(user=request.user, month=month, year=year).first()
        if existing_budget:
            return Response({"detail": "Budget already exists for this month/year."}, status=status.HTTP_400_BAD_REQUEST)

        budget = Budget.objects.create(
            user=request.user,
            month=month,
            year=year,
            amount=amount
        )
        serializer = BudgetSerializer(budget)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, budget_id, *args, **kwargs):
        """
        Updates an existing budget.
        """
        try:
            budget = Budget.objects.get(id=budget_id, user=request.user)
            serializer = BudgetSerializer(budget, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Budget.DoesNotExist:
            raise NotFound(detail="Budget not found.")

    def delete(self, request, budget_id, *args, **kwargs):
        """
        Deletes a specific budget.
        """
        try:
            budget = Budget.objects.get(id=budget_id, user=request.user)
            budget.delete()
            return Response({"detail": "Budget deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Budget.DoesNotExist:
            raise NotFound(detail="Budget not found.")

class BudgetSummaryView(APIView):
    """
    API view to retrieve the summary of the user's budget for a specific month and year.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieves the budget summary for a given month and year.
        """
        try:
            month = int(request.query_params.get('month', datetime.today().month))
            year = int(request.query_params.get('year', datetime.today().year))
        except ValueError:
            return Response({"detail": "Month and year must be integers."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to retrieve the budget for the given month and year
            budget = Budget.objects.get(user=request.user, month=month, year=year)
            remaining = budget.amount - budget.spent_amount
            return Response({
                "month": month,
                "year": year,
                "budget_amount": round(budget.amount, 2),
                "spent_amount": round(budget.spent_amount, 2),
                "remaining_amount": round(remaining, 2)
            }, status=status.HTTP_200_OK)

        except Budget.DoesNotExist:
            return Response({
                "month": month,
                "year": year,
                "budget_amount": 0,
                "spent_amount": 0,
                "remaining_amount": 0
            }, status=status.HTTP_200_OK)

class SpendingByCategoryView(APIView):
    """
    API view to retrieve spending data grouped by category.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieves spending data grouped by transaction category.
        """
        transactions = Transaction.objects.filter(user=request.user, category__isnull=False)

        if not transactions.exists():
            return Response({"detail": "No spending data available."}, status=status.HTTP_200_OK)

        category_spending = defaultdict(Decimal)

        for txn in transactions:
            category_spending[txn.category] += txn.amount

        result = [{"category": k, "amount": round(v, 2)} for k, v in category_spending.items()]

        return Response(result, status=status.HTTP_200_OK)

class TotalExpensesOverTimeAPIView(APIView):
    """
    API view to retrieve the total expenses over time, grouped by month.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves the total expenses over time, grouped by month and formatted as YYYY-MM.
        """
        expenses = (
            Transaction.objects.filter(user=request.user)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total_spent=Sum('amount'))
            .order_by('month')
        )

        # Format month as string YYYY-MM for frontend chart compatibility
        formatted = [
            {
                "month": expense["month"].strftime("%Y-%m"),
                "total_spent": expense["total_spent"]
            }
            for expense in expenses
        ]

        return Response(formatted)
