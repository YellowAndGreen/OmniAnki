from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.CharField(max_length=200000, blank=False)
    top_image_url = models.CharField(max_length=200, default="none")

    class Meta:
        ordering = ('-id',)


class Book(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.BinaryField(blank=False)
    progress = models.FloatField(default=0, blank=False)
    top_image_url = models.CharField(max_length=200, default="none")
