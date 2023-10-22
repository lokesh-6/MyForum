from django.urls import path
from . import views
urlpatterns=[
    path('' , views.home,name='home'),
    path('details/<slug:slug>/' , views.details,name='detail'),
    path('posts/<slug:slug>/' , views.posts,name='posts'),
    path('create_post' , views.create_post,name='create_post'),
    
]