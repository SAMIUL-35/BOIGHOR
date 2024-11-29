# In views.py
from django.shortcuts import render, get_object_or_404
from Book.models import BookModel
from category.models import CategoryModel

def Home(request, slug=None):
    # Fetch all books by default
    data = BookModel.objects.all()
    category = None  # Default to None if no category is selected

    # If a slug is provided, filter books by the category
    if slug:
        category = get_object_or_404(CategoryModel, slug=slug)
        data = BookModel.objects.filter(category=category)
    
    # Fetch all categories for display or filtering purposes
    categories = CategoryModel.objects.all()
    
    return render(request, 'index.html', {
        'data': data,
        'categories': categories,
        'selected_category': category
    })
