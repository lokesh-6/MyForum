from django.shortcuts import render,get_object_or_404,redirect

from .models import Author,Category,Post,Comment,Reply
from .utils import update_views

from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.

def home(request):
    forums=Category.objects.all()

    return render(request,'home.html',{'post':forums})

@login_required
def details(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST" and "comment-form" in request.POST:
        comment_content = request.POST.get("comment-form")
        user = request.user
        author, created = Author.objects.get_or_create(user=user)
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment_content)
        new_comment.save()
        post.comments.add(new_comment)

    update_views(request,post)

    if request.method == "POST" and "reply-form" in request.POST:
        reply_content = request.POST.get("reply-form")
        comment_id=request.POST.get("comment-id")
        comment_obj=Comment.objects.get(id=comment_id)
        if request.user.is_authenticated:
            author, created = Author.objects.get_or_create(user=request.user)

        # Ensure author is defined even if the user is not authenticated
        if not author:
            author = None
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply_content)
        comment_obj.replies.add(new_reply.id)
    update_views(request,post)
    return render(request, 'details.html', {'post': post})

def posts(request,slug):

    category=get_object_or_404(Category,slug=slug)
    posts=Post.objects.filter(approved=True,categories=category)
    paginator=Paginator(posts,5)
    page=request.GET.get("page")
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    
    return render(request,'posts.html',{'post':posts})

@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()

            # Save categories and tags separately after the post is saved
            form.save_m2m()  # This will save the many-to-many relationships (categories and tags)

            return redirect('home')

    context.update({
        "form": form,
        "title": "Create New Post",
    })
    return render(request, "create_post.html", context)