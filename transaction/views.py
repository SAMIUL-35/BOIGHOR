from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps
from .models import UserDepositAccount
from .forms import DepositForm
from Book.models import BookModel

def send_transaction_email(user, amount, subject, template):
    try:
        message = render_to_string(template, {'user': user, 'amount': amount})
        email = EmailMultiAlternatives(subject, '', to=[user.email])
        email.attach_alternative(message, "text/html")
        email.send()
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

@login_required
def deposit_view(request):
    try:
        account = UserDepositAccount.objects.get(user=request.user)
    except UserDepositAccount.DoesNotExist:
        return render(request, 'transaction/deposit.html', {
            'error_message': "You do not have a deposit account. Please create one."
        })

    form = DepositForm(request.POST or None)
    error_message = None
    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']
        try:
            account.deposit(amount)
            send_transaction_email(
                user=request.user,
                amount=amount,
                subject="Deposit Confirmation",
                template="transaction/deposit_email.html"
            )
            return render(request, 'transaction/deposit.html', {
                'form': DepositForm(),
                'account': account,
                'success_message': f"Successfully deposited ${amount}"
            })
        except Exception as e:
            error_message = str(e)
    return render(request, 'transaction/deposit.html', {
        'form': form,
        'account': account,
        'error_message': error_message
    })

@login_required
def borrow_book_view(request, book_id):
    account = get_object_or_404(UserDepositAccount, user=request.user)
    book = get_object_or_404(BookModel, id=book_id)

    if book.is_borrowed:
        messages.error(request, f"The book '{book.title}' is already borrowed.")
        return redirect('home')

    if book.borrowing_price > account.balance:
        messages.error(request, f"Insufficient balance to borrow the book '{book.title}'. Please deposit funds.")
        return redirect('deposit_money')

    try:
        account.balance -= book.borrowing_price
        account.save()
        book.borrowed_by = request.user
        book.is_borrowed = True
        book.save()
        Transaction = apps.get_model('transaction', 'Transaction')
        Transaction.objects.create(
            account=account,
            book=book,
            description="Borrowed book",
            amount=-book.borrowing_price,
            balance_after_transaction=account.balance
        )
        send_transaction_email(
            user=request.user,
            amount=book.borrowing_price,
            subject="Book Borrowed",
            template="transaction/borrow_email.html"
        )
        messages.success(request, f"You have successfully borrowed the book '{book.title}'.")
        return redirect('profile')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

@login_required
def return_book_view(request, book_id):
    account = get_object_or_404(UserDepositAccount, user=request.user)
    book = get_object_or_404(BookModel, id=book_id)

    if book.borrowed_by != request.user:
        return JsonResponse(
            {"error": f"You cannot return '{book.title}' because it is not borrowed by you."},
            status=403
        )

    try:
        account.balance += book.borrowing_price
        account.save()
        book.borrowed_by = None
        book.is_borrowed = False
        book.save()
        Transaction = apps.get_model('transaction', 'Transaction')
        Transaction.objects.create(
            account=account,
            book=book,
            description="Returned book",
            amount=book.borrowing_price,
            balance_after_transaction=account.balance
        )
        send_transaction_email(
            user=request.user,
            amount=book.borrowing_price,
            subject="Book Returned",
            template="transaction/return_email.html"
        )
        return JsonResponse(
            {"success": f"Successfully returned '{book.title}'."},
            status=200
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"An error occurred while returning the book: {str(e)}"},
            status=500
        )

@login_required
def transaction_list_view(request):
    account = get_object_or_404(UserDepositAccount, user=request.user)
    transactions = account.transactions.all()
    return render(request, 'transaction/transactions.html', {'transactions': transactions})
