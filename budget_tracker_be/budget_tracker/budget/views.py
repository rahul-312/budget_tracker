from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction, Budget
from .serializers import TransactionSerializer, BudgetSerializer
from rest_framework.exceptions import NotFound

from .models import CategoryType


class CategoryChoicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        choices = [
            {"value": choice[0], "label": choice[1]}
            for choice in CategoryType.choices
        ]
        return Response(choices)

class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id=None, *args, **kwargs):
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
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, transaction_id, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
            serializer = TransactionSerializer(transaction, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Transaction.DoesNotExist:
            raise NotFound(detail="Transaction not found.")

    def delete(self, request, transaction_id, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
            transaction.delete()
            return Response({"detail": "Transaction deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Transaction.DoesNotExist:
            raise NotFound(detail="Transaction not found.")

class BudgetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, budget_id=None, *args, **kwargs):
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
        try:
            budget = Budget.objects.get(id=budget_id, user=request.user)
            budget.delete()
            return Response({"detail": "Budget deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Budget.DoesNotExist:
            raise NotFound(detail="Budget not found.")
