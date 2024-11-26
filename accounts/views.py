from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.views.generic import CreateView, UpdateView, TemplateView
from .forms import RegisterForm, ChangeUserForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
# from car.models import CarModel
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




class Register(CreateView):
    form_class = RegisterForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Registration successful! Please log in.')
        return super().form_valid(form)

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
class profile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
       
        
        # context['cars'] = CarModel.objects.filter(purchased_by=self.request.user)  
        return context


class user_Logout(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Logged out successfully.')
        response = super().dispatch(request, *args, **kwargs)
        return redirect('home')
