from django.views.generic import DetailView
from .models import BookModel, Review

class DetailView(DetailView):
    model = BookModel
    template_name = "detail.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        # Fetch the default context
        context = super().get_context_data(**kwargs)

        # Get the current book object
        book = self.get_object()

        # Fetch all reviews for the book
        reviews = Review.objects.filter(book=book).order_by('-created_at')

        # Check if the user is authenticated and has borrowed the book
        can_review = (
            self.request.user.is_authenticated
            and book.borrowed_by == self.request.user
            and book.is_borrowed
        )

        # Add reviews and can_review to the context
        context['reviews'] = reviews
        context['can_review'] = can_review

        return context
