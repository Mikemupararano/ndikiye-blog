from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),  # include app urls
    path('', RedirectView.as_view(pattern_name='blog:post_list', permanent=False)),  # root → blog list
]
