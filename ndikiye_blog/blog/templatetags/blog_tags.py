from django import template
from ..models import Post

# Create a custom template tag library
register = template.Library()

@register.simple_tag
def total_posts():
    """Return total number of published posts."""
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """Return latest published posts."""
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}
