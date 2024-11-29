from django.urls import path
from .views import review_book

urlpatterns = [
    path('<int:book_id>/review/', review_book, name='review_book'),  # Path with book_id
]
