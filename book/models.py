from django.contrib.postgres.fields import ArrayField
from django.db import models

class Book(models.Model):
    id = models.CharField(primary_key=True, max_length=55)
    title = models.CharField(max_length=255)
    authors = ArrayField(models.TextField(), null=True)
    published_date = models.CharField(max_length=10)
    categories = ArrayField(models.TextField(), null=True)
    average_rating = models.FloatField(default=0.0)
    ratings_count = models.IntegerField(default=0)
    thumbnail = models.URLField()