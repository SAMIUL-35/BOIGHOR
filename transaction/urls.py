from django.urls import path
from .views import deposit_view, borrow_book_view, transaction_list_view, return_book_view

urlpatterns = [
    path("deposit/", deposit_view, name="deposit_money"),  
    path("borrow/<int:book_id>/", borrow_book_view, name="borrow_book"),  
    path("return/<int:book_id>/", return_book_view, name="return_book"),  
    path("report/", transaction_list_view, name="transaction_report"),  
]
