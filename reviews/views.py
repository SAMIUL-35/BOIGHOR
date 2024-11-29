from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Book.models import BookModel
from .forms import ReviewForm
from .models import Review



@login_required
def review_book(request, book_id):
    book = get_object_or_404(BookModel, id=book_id)
    reviews = Review.objects.filter(book=book).order_by('-created_at')  # Fetch all reviews for the specific book
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted!")
            return redirect('detail', id=book.id)
    else:
        form = ReviewForm()

    return render(request, 'detail.html', {'object': book, 'reviews': reviews, 'form': form})
