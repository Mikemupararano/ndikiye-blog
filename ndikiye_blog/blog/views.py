from django.core.paginator import EmptyPage,PageNotAnInteger , Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views import ListView

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

class PostListView(ListView):
    """
    Alternative class-based view for listing published posts.
    """
    queryset = Post.published.all()  # Uses your custom PublishedManager
    context_object_name = 'posts'
    paginate_by = 3  # 3 posts per page
    template_name = 'blog/post/list.html'
    
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
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    
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
