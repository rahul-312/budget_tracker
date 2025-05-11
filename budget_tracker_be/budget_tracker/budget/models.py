from django.db import models
from django.conf import settings

class CategoryType(models.TextChoices):
    """
    Enum-like class representing various categories for transactions.
    These categories are used to classify different types of expenses or income.
    """
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
    """
    Model representing a financial transaction made by a user.
    
    Attributes:
        user (ForeignKey): The user who made the transaction.
        amount (DecimalField): The amount of money involved in the transaction.
        category (CharField): The category of the transaction, chosen from predefined categories.
        description (TextField): A description of the transaction (optional).
        date (DateField): The date the transaction occurred, automatically set to the current date.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CategoryType.choices, default=CategoryType.OTHER)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the Transaction instance.
        
        Returns:
            str: A string containing the user's name, the transaction category, and the amount.
        """
        return f"{self.user} - {self.category} - {self.amount}"
    

class Budget(models.Model):
    """
    Model representing a user's budget for a specific month and year.
    
    Attributes:
        user (ForeignKey): The user who owns the budget.
        amount (DecimalField): The total budgeted amount for the given period.
        spent_amount (DecimalField): The amount already spent from the budget, default is 0.00.
        month (PositiveSmallIntegerField): The month for which the budget is set (1-12).
        year (PositiveIntegerField): The year for which the budget is set.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveIntegerField()

    def __str__(self):
        """
        String representation of the Budget instance.
        
        Returns:
            str: A string containing the user's name, the budget category, and the month/year.
        """
        return f"{self.user} - {self.month}/{self.year} - {self.amount}"
