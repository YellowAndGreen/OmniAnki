from django.contrib import admin
from .models import Card


# Register your models here.
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'question']
    # prepopulated_fields = {'slug': ('title',)}
