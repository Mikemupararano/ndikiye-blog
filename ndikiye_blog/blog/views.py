from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def post_detail(request, year, month, day, post):
    """
    Displays the details for a single published post identified
    by its slug and publication date.
    """
    post = get_object_or_404(
        Post,
        slug=post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )


def post_list(request):
    """
    Displays a list of all published blog posts.
    """
    post_list = Post.published.all()  # Uses your custom PublishedManager
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)  # Show 3 posts per page.
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def index(request):
    """
    Displays the blog's index page (or redirects/links to post list).
    """
    return render(request, 'blog/index.html')
