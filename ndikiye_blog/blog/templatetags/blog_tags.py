from django import template
from ..models import Post
# Create a custom template tag to get the total number of published posts
register = template.Library()
@register.simple_tag
def total_posts():
    return Post.published.count()

