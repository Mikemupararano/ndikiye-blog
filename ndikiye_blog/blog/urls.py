from django.urls import path
from . import views  # import your view functions

app_name = 'blog'  # required if you use namespace='blog' in project urls

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path(
        'post/<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'
    ),
    path('index/', views.index, name='index'),
]
