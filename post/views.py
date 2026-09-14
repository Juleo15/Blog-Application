from django.shortcuts import redirect, render
from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import get_object_or_404

from post.form import PostForm
from .models import Post

# Create your views here.

def post_list(request):
    post = Post.objects.all()
    try:
        paginator = Paginator(post, 2)
        page_number = request.GET.get('page')
        post = paginator.get_page(page_number)
    except PageNotAnInteger:
        post = Post.objects.all()
    except Exception as e:
        print(f"An error occurred: {e}")
        post = paginator.page(1)
    
    context = {
        'posts': post,
        'paginator': paginator
    }
    return render(request, 'post/post_list.html', context)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
  
    return render(
        request,
        "post/post_detail.html",
        {"post": post}
    )
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect("post:post_list")
    else:
        form = PostForm()
    return render(request, "post/post_create.html", {"form": form})