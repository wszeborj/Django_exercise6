from typing import Any
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.http import JsonResponse
from .models import Book
from .serializers import BookSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.decorators import action


@csrf_exempt
def update_db(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={data}')
        data_external: dict[str, Any] = response.json()
        books_data = data_external.get('items', [])

        for book_data in books_data:
            volume_info = book_data.get('volumeInfo', {})
            book_id = book_data.get('id', '')

            book, created = Book.objects.get_or_create(id=book_id)
            book.title = volume_info.get('title', '')
            book.authors = volume_info.get('authors', [])
            book.published_date = volume_info.get('publishedDate', '')
            book.categories = volume_info.get('categories', [])
            book.average_rating = volume_info.get('averageRating', 0.0)
            book.ratings_count = volume_info.get('ratingsCount', 0)
            book.thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', '')

            book.save()

        return JsonResponse({'message': 'Data imported successfully.'})

    return JsonResponse({'message': 'Invalid request Method'})

class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        authors: list[str] = self.request.GET.getlist("author")
        if authors:
            if authors[0][0] == "\"" and authors[0][0] == "\"":
                authors = [author[1:-1] for author in authors]
            queryset = queryset.filter(authors=authors)

        published_date = self.request.GET.get("published_date")
        if published_date:
            queryset = queryset.filter(published_date=published_date)

        sort = self.request.GET.get("sort")
        if sort:
            queryset = queryset.order_by(sort)

        return queryset

    @action(methods=['POST'], detail=False, url_path='db')
    def download_db(self, request, *args, **kwargs):
        data = json.loads(request.body)
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={data}')
        data_external: dict[str, Any] = response.json()
        books_data = data_external.get('items', [])

        for book_data in books_data:
            volume_info = book_data.get('volumeInfo', {})
            book_id = book_data.get('id', '')

            book, created = Book.objects.get_or_create(id=book_id)
            book.title = volume_info.get('title', '')
            book.authors = volume_info.get('authors', [])
            book.published_date = volume_info.get('publishedDate', '')
            book.categories = volume_info.get('categories', [])
            book.average_rating = volume_info.get('averageRating', 0.0)
            book.ratings_count = volume_info.get('ratingsCount', 0)
            book.thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', '')

            book.save()
            return JsonResponse({'message': 'Data imported successfully.'})

        return JsonResponse({'message': 'Invalid request Method'})

#
#
# def get_books(request):
#     if request.method == 'GET':
#         filtered_books = Book.objects.all()
#
#         authors :list[str] = request.GET.getlist("author")
#         if authors:
#             if authors[0][0] == "\"" and authors[0][0] == "\"":
#                 authors = [author[1:-1] for author in authors]
#             filtered_books = Book.objects.filter(authors=authors)
#
#         published_date = request.GET.get("published_date")
#         if published_date:
#             filtered_books = Book.objects.filter(published_date=published_date)
#
#         sort = request.GET.get("sort")
#         if sort:
#             filtered_books = Book.objects.order_by(sort)
#
#         serializer = BookSerializer(filtered_books, many=True)
#
#         return JsonResponse(serializer.data, safe=False)
#
# def get_book(request, book_id):
#     if request.method == 'GET':
#         try:
#             filtered_book = Book.objects.get(id=book_id)
#             serializer = BookSerializer(filtered_book, many=False)
#
#             return JsonResponse(serializer.data)
#         except Book.DoesNotExist:
#             return JsonResponse({'message': 'Book not found.'}, status=404)