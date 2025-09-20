from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),              # resolves as /blog/
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('index/', views.index, name='index'),
]
