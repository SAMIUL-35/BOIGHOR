from django.db import models
from accounts.models import UserDepositAccount
from Book.models import BookModel  # Assuming 'BookModel' is in the 'category' app

class Transaction(models.Model):
    account = models.ForeignKey(UserDepositAccount, related_name='transactions', on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, related_name='transactions', on_delete=models.SET_NULL, null=True, blank=True)  # Link to BookModel
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.description} - {self.amount} on {self.timestamp}"
