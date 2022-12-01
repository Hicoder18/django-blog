from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
    path('comment', views.comment, name='comment'),
    path('comment/<int:es_id>', views.comment, name='comment'),
]
