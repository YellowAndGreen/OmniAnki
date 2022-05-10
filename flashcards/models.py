import datetime

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


# import datetime


class Card(models.Model):
    group = models.CharField(max_length=20)
    question = models.CharField(max_length=200, default="none", blank=False)
    answer = models.CharField(max_length=200, default="none", blank=False)
    example = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)
    extra = models.CharField(max_length=200)
    tags = TaggableManager()
    due = models.DateTimeField(null=False, default=datetime.date(1900, 1, 1))
    review_num = models.PositiveIntegerField(null=False, default=0)
    forget_num = models.PositiveIntegerField(null=False, default=0)
    ratio = models.PositiveIntegerField(null=False, default=0)
    interval = models.PositiveIntegerField(null=True, default=0, blank=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ('id',)
        # verbose_name = 'category'
        # verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('flashcards:card_detail',
                       args=[self.id])


# 每次使用时的数据，作为外键与卡片绑定
class Recitedata(models.Model):
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    rank = models.PositiveIntegerField(verbose_name="easy or diff?", default=0)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="recitedata")
    params = models.CharField(max_length=20000, default='{}')

    def __str__(self):
        return str(self.date) + ":" + str(self.rank)

    class Meta:
        ordering = ('date',)


class WordList(models.Model):
    owner = models.ForeignKey(User, models.CASCADE, related_name='owner')
    name = models.CharField(max_length=20, blank=False)
    wordlist = models.CharField(max_length=20000, blank=False)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    progress = models.PositiveIntegerField(blank=False, default=0)
    len_list = models.PositiveIntegerField(blank=False, default=50)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('date',)


class Settings(models.Model):
    random_example = models.BooleanField(default=False)
    user = models.ForeignKey(User, models.CASCADE, related_name='settings')
    current_group = models.CharField(max_length=1000, default='{}')


class Dict(models.Model):
    headword = models.CharField(max_length=2000, blank=False)
    item = models.CharField(max_length=200000, blank=False)
    # coca排名
    coca = models.PositiveIntegerField(blank=False, default=0)
