from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib import messages
from .models import BookModel
from django.shortcuts import get_object_or_404, redirect

from django.views.generic import DetailView
from .models import BookModel, Review

class DetailView(DetailView):
    model = BookModel
    template_name = "detail.html"
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current book object
        book = self.get_object()

        # Fetch the reviews for the book
        reviews = Review.objects.filter(book=book).order_by('-created_at')
        
        # Add reviews to the context
        context['reviews'] = reviews

        return context


