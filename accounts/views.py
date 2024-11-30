from .models import UserDepositAccount
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, TemplateView
from .forms import RegisterForm, ChangeUserForm
from Book.models import BookModel


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        UserDepositAccount.objects.create(user=user)
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
        return super().get_object(queryset)

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class pass_change(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'pass_change.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class Profile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        account = UserDepositAccount.objects.filter(user=user).first()
        if not account:
            account = UserDepositAccount.objects.create(user=user)
        transactions = account.transactions.all() if account else []
        books = BookModel.objects.filter(borrowed_by=user, is_borrowed=True)
        context['user'] = user
        context['transactions'] = transactions
        context['books'] = books
        context['account'] = account
        return context


class user_Logout(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Logged out successfully.')
        super().dispatch(request, *args, **kwargs)
        return redirect('home')
