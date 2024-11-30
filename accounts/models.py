from django.contrib.auth.models import User
from django.db import models
from django.apps import apps
import random
from Book.models import BookModel


class UserDepositAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_no = models.IntegerField(unique=True, editable=False)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    initial_deposite_date = models.DateField(auto_now_add=True)

    def generate_account_no(self):
        while True:
            account_no = random.randint(100000, 999999)
            if not UserDepositAccount.objects.filter(account_no=account_no).exists():
                return account_no

    def save(self, *args, **kwargs):
        if not self.account_no:
            self.account_no = self.generate_account_no()
        super().save(*args, **kwargs)

    def deposit(self, amount):
        Transaction = apps.get_model('transaction', 'Transaction')
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.save()
        Transaction.objects.create(
            account=self,
            description="Deposit",
            amount=amount,
            balance_after_transaction=self.balance
        )

    def borrow_book(self, book):
        Transaction = apps.get_model('transaction', 'Transaction')
        if book.borrowing_price > self.balance:
            raise ValueError(f"Insufficient balance to borrow the book '{book.title}'.")
        self.balance -= book.borrowing_price
        self.save()
        Transaction.objects.create(
            account=self,
            book=book,
            description=f"Borrowed book: {book.title}",
            amount=-book.borrowing_price,
            balance_after_transaction=self.balance
        )

    def return_book(self, book):
        Transaction = apps.get_model('transaction', 'Transaction')
        self.balance += book.borrowing_price
        self.save()
        Transaction.objects.create(
            account=self,
            book=book,
            description=f"Returned book: {book.title}",
            amount=book.borrowing_price,
            balance_after_transaction=self.balance
        )

    def __str__(self):
        return f"Account {self.account_no} ({self.user.username})"
