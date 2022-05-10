from django.urls import path

from todo.views import *

app_name = 'todo'
urlpatterns = [
    path('', index, name='index'),

]
