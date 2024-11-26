from django.urls import path,include
from . import views

urlpatterns = [
  
    path('register/', views.Register.as_view(),name='register'),
    path('login/', views.user_login.as_view(),name='login'),
    path('logout/', views.user_Logout.as_view(next_page='home'),name='logout'),
    path('profile/', views.profile.as_view(),name='profile'),
    path('edit-profile/<int:id>/', views.update_user.as_view(), name='edit_profile'),
    path('pass_change/<int:id>/', views.pass_change.as_view(), name='pass_change'),
    
]