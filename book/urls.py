from django.urls import path
from .views import update_db, BookViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'books', BookViewSet)


urlpatterns = [
        path('db', update_db, name='update_db'),
        # path('books/', get_books, name='get_books'),
        # path('books/<str:book_id>', get_book, name='get_book'),
] + router.urls