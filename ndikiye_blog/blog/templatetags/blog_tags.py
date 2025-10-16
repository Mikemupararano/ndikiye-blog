from django import template
from ..models import Post
from django.db.models import Count

# Create a custom template tag library
register = template.Library()

@register.simple_tag
def total_posts():
    """Return total number of published posts."""
    return Post.published.count()
# Creating a template tag that returns the most commented posts
@register.simple_tag
def get_most_commented_posts(count=5):
    """Return most commented published posts."""
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """Return latest published posts."""
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}
