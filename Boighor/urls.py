# In your urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from core.views import Home

urlpatterns = [
    path('', Home, name='home'),  # Default homepage view
    path('category/<slug:slug>/', Home, name='home'),  # Category-specific view (optional slug)
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('reviews/', include('reviews.urls')),
    path('book/', include('Book.urls')),
    path('transaction/', include('transaction.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
