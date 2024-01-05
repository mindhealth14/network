from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,  get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib import messages  # Import messages for feedback
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import PostSerializer  # You may need to create a serializer
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import User, Post
from .forms import PostForm, PostUpdateForm
from followers.models import Follower
from django.core.paginator import Paginator



def feed(request):
    post_list = Post.objects.all().order_by('-id')
    #paginator with 3 post
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    return render(request, "network/homepage.html", {
        'posts': posts,
    })



def following_post(request):
    if request.user.is_authenticated:
        following = (
            Follower.objects.filter(followed_by=request.user).values_list('following', flat=True)
        )

        if not following:
            # If the user is not following anyone, show default posts.
            post_list = Post.objects.all().order_by('-id')
        else:
            post_list = Post.objects.filter(author__in=following).order_by('-id')
    else:
        # If the user is not authenticated, show default posts.
        post_list = Post.objects.all().order_by('-id')
        
    

    # Pagination logic
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)

    return render(request, "network/follow_post.html", {
      'posts': posts,
    })


def my_post(request):
    user = request.user
    my_post = Post.objects.filter(author=user).order_by('-id')[0:10]
    return render(request, 'network/my_post.html', {
        'my_post': my_post, 
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


class CreateNewPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "feed/create.html"
    fields = ['text']
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        # TODO: There is a bug here when you go to /new/ to create a post.
        # You must figure out how to determine if this is an Ajax request (or not an ajax request).
        post = Post.objects.create(
            text=request.POST.get("text"),
            author=request.user,
        )

        return render(
            request,
            "network/post.html",
            {
                "post": post,
              
            },
            content_type="application/html"
        )
 
 
 
 #Likes and unlikes    
def post_likes(request, post_id):
    
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)

        # Check if the user has already liked this post
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            status = 'unliked'
        else:
            post.likes.add(request.user)
            status = 'liked'
        
        return JsonResponse({'status': status })
        
    return JsonResponse({'status': 'error'})


# Like Count
def like_count(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=post_id )
        like_count = post.likes.count()  # Changed variable name to snake_case
        return JsonResponse({'likeCount': like_count})
        

@login_required
def post_details(request, post_id):
    posts = get_object_or_404(Post, post_id)
    return render(request, 'network/post_details', {
        'posts': posts
    })


@login_required
def edit_post(request, post_id):
    pass




def delete_post(request, post_id):
    pass
    
    