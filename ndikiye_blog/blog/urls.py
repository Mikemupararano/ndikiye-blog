from django.urls import path
from . import views  # import your view functions

app_name = 'blog'  # required if you use namespace='blog' in project urls

urlpatterns = [
    # Post list view - using class-based view
    
    # path('', views.PostListView.as_view(), name='post_list'),
    # Post list view - using function-based view
     path('', views.post_list, name='post_list'),
     path(
         'tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'
         ),
    path(
        'post/<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'
    ),
    path('post/<int:post_id>/share/', views.post_share, name='post_share'),
    path(
        'post/<int:post_id>/comment/', views.post_comment, name='post_comment'
    ),
    # path('index/', views.index, name='index'),
]
