from django.contrib.auth.models import User
from django.db import models
from category.models import CategoryModel
from reviews.models import Review

class BookModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='book_images/')
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True) 
    borrowed_by = models.ForeignKey(User,related_name='user', on_delete=models.CASCADE, null=True, blank=True)
    is_borrowed = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.title
