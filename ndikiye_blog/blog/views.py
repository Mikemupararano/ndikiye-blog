from django.core.paginator import EmptyPage,PageNotAnInteger , Paginator
from django.shortcuts import render, get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.decorators
from .models import Post
from django.views.generic import ListView
# from forms import EmailPostForm
from .forms import CommentForm, EmailPostForm
from django.core.mail import send_mail

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
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form
        }
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
    """Creating an instance of the form to handle form submission
    """
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
                )
            # ... send email
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
            
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {'post': post,
         'form': form,
         'sent': sent
         }
        )
@require_POST
def post_comment(request, post_id):
    """
    Handles the submission of a comment form for a specific post.
    """
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create Comment object but don't save to database yet
        comment = form.save(commit=False)
        # Assign the current post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {'post': post,
         'form': form,
         'comment': comment}
    )