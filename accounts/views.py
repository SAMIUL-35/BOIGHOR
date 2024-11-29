

# Create your views here.
from .models import UserDepositAccount, BookModel
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.views.generic import CreateView, UpdateView, TemplateView
from .forms import RegisterForm, ChangeUserForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from Book.models import BookModel
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import UserDepositAccount
from .forms import RegisterForm

class Register(CreateView):
    form_class = RegisterForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Save the user instance first
        response = super().form_valid(form)
        user = form.instance

        # Create a UserDepositAccount for the new user
        UserDepositAccount.objects.create(user=user)

        # Add a success message
        messages.success(self.request, 'Registration successful! Your account has been created. Please log in.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Sign Up'
        return context


class user_login(LoginView):
    template_name = 'registration.html'

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Login information incorrect. Please try again.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Sign in'
        return context
    
    
@method_decorator(login_required, name='dispatch')
class update_user(UpdateView):
    form_class = ChangeUserForm
    model = User
    template_name = 'update_user.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        print(f"Fetched User: {obj.username}, {obj.first_name}, {obj.last_name}")  
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)
    
    
@method_decorator(login_required, name='dispatch')
class pass_change(PasswordChangeView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'pass_change.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)





@method_decorator(login_required, name='dispatch')



class Profile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current logged-in user
        user = self.request.user

        # Get the user's deposit account, or create a new one if it doesn't exist
        account = UserDepositAccount.objects.filter(user=user).first()  # Use filter to prevent 404
        if not account:
            # If no account is found, create a default one or handle accordingly
            account = UserDepositAccount.objects.create(user=user)

        # Get all transactions related to this user's account
        transactions = account.transactions.all() if account else []

        # Get books currently borrowed by the user
        books = BookModel.objects.filter(borrowed_by=user, is_borrowed=True)  # Ensure is_borrowed field is used

        # Add user, transactions, and books to the context
        context['user'] = user
        context['transactions'] = transactions
        context['books'] = books
        context['account'] = account  # Add account to context for display in profile

        return context


class user_Logout(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Logged out successfully.')
        response = super().dispatch(request, *args, **kwargs)
        return redirect('home')
