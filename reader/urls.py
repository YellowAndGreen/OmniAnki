from django.urls import path

from reader.views import *

app_name = 'reader'
urlpatterns = [
    # path('', index, name='dashboard'),
    # path('<slug:category_slug>/', views.product_list, name="product_list_by_category"),
    path('article/<int:article_id>/', article_detailview, name='article_detailview'),
    path('', article_list, name='article_list'),
    path('update_article/', update_article, name='update_article'),
    path('book/', read_book, name='read_book'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('book_progress/', book_progress, name='book_progress'),
]
