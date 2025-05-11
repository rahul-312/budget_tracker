from django.db import models
from django.conf import settings

class CategoryType(models.TextChoices):
    FOOD = "Food", "Food"
    TRAVEL = "Travel", "Travel"
    SHOPPING = "Shopping", "Shopping"
    NECESSITIES = "Necessities", "Necessities"
    ENTERTAINMENT = "Entertainment", "Entertainment"
    TRANSPORTATION = "Transportation", "Transportation"
    INSURANCE = "Insurance", "Insurance"
    MEDICAL = "Medical", "Medical"
    EDUCATION = "Education", "Education"
    GIFT = "Gift", "Gift"
    INVESTMENTS = "Investments", "Investments"
    OTHER = "Other", "Other"


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CategoryType.choices, default=CategoryType.OTHER)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.category} - {self.amount}"
    

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    month = models.PositiveSmallIntegerField()  # 1 = January, 12 = December
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} - {self.category} - {self.month}/{self.year}"