from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from .models import *

from django.views.generic import ListView

class PostList(ListView):
    paginate_by = 5
    model = Post


def index(request):
    if request.method == "POST":
        content = request.POST["content"]

        if not content:
            return render(request, "network/index.html", {
                'message': 'Must provide content.'
            })
        elif not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        

        new_post = Post(
            poster = User.objects.get(username=request.user),
            content = content
        )
        new_post.save()

    # code (idea) from https://docs.djangoproject.com/en/3.0/topics/pagination/
    posts_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    num_pages = paginator.num_pages

    return render(request, 'network/index.html', {
        'page_obj': page_obj,
        'num_pages': range(1, num_pages + 1)
    })

# def ownprofile(request):
#     return HttpResponseRedirect(reverse("index"))


def profile(request, **username):
    if not username:
        username = request.user
    else:
        username = username['username']

    
    try:
        username = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist!")

    posts_list = Post.objects.filter(poster=username).order_by('-timestamp')
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    num_pages = paginator.num_pages

    return render(request, 'network/profile.html', {
        'username': username,
        'page_obj': page_obj,
        'num_pages': range(1, num_pages + 1),
        'num_posts': posts_list.count()
    })


@csrf_exempt
def follow(request, username):
    followed_user = User.objects.get(username=username)
    follower_user = User.objects.get(username=request.user)

    followed = Follow.objects.get(user=followed_user)
    follower = Follow.objects.get(user=follower_user)

    followed.followers.add(follower_user)
    follower.following.add(followed_user)

    print('hi')



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
            user = Follow(username)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
