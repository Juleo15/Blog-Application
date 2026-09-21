from django.shortcuts import redirect, render
from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.db.models import F
import json
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


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

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
  
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
def post_vote(request, pk, vote_type):
    post = get_object_or_404(Post, pk=pk)

    if vote_type == "like":
        post.likes = F('likes') + 1
    elif vote_type == "dislike":
        post.dislikes = F('dislikes') + 1

    post.save()
    return redirect(request.META.get('HTTP_REFERER', 'post:post_list'))

@require_POST
def post_share(request, pk):
    post = get_object_or_404(Post, pk=pk)

    raw_emails = request.POST.get('emails', '')
    message = request.POST.get('message', '')

    # Split by comma, strip whitespace, drop empty entries
    emails = [e.strip() for e in raw_emails.split(',') if e.strip()]

    if not emails:
        return JsonResponse({'success': False, 'error': 'Enter at least one email.'})

    post_url = request.build_absolute_uri(post.get_absolute_url())
    subject = f"{request.user if request.user.is_authenticated else 'Someone'} shared a post: {post.title}"
    body = f"{message}\n\nRead it here: {post_url}"

    try:
        send_mail(
            subject,
            body,
            None,  # uses DEFAULT_FROM_EMAIL from settings.py
            emails,
            fail_silently=False,
        )
    except Exception:
        return JsonResponse({'success': False, 'error': 'Could not send email. Try again later.'})

    return JsonResponse({'success': True})