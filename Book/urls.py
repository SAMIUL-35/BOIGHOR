from django.urls import path
from .views import DetailView 

urlpatterns = [
    path('book/<int:id>/', DetailView.as_view(), name='detail'),

]