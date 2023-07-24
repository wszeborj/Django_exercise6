from django.urls import path
from .views import update_db, get_books, get_book

urlpatterns = [
        path('db', update_db, name='update_db'),
        path('books/', get_books, name='get_books'),
        path('books/<str:book_id>', get_book, name='get_book'),
]