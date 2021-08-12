from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from .models import *

from django.views.generic import ListView

class PostList(ListView):
    paginate_by = 10
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

        return HttpResponseRedirect(reverse("index"))

    # code (idea) from https://docs.djangoproject.com/en/3.0/topics/pagination/
    posts_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
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

    print(username)
    
    try:
        username = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist!")

    posts_list = Post.objects.filter(poster=username).order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    num_pages = paginator.num_pages


    follow = Follow.objects.get(user=username)
    # followers = list(followers.followers.all())
    if request.user in list(follow.followers.all()):
        is_following = True
    else:
        is_following = False

    return render(request, 'network/profile.html', {
        'username': username,
        'followers': follow.followers.all().count(),
        'following': follow.following.all().count(),
        'page_obj': page_obj,
        'num_pages': range(1, num_pages + 1),
        'num_posts': posts_list.count(),
        'is_following': is_following
    })


@csrf_exempt
@login_required
def follow(request, username):
    followed_user = User.objects.get(username=username)
    follower_user = User.objects.get(username=request.user)

    followed = Follow.objects.get(user=followed_user)
    follower = Follow.objects.get(user=follower_user)


    action = json.loads(request.body).get('action')

    if action == "follow":
        followed.followers.add(follower_user)
        follower.following.add(followed_user)
    elif action == "unfollow":
        followed.followers.remove(follower_user)
        follower.following.remove(followed_user)


    return HttpResponseRedirect(reverse("profile", args=(username,)))


@login_required
def following(request):
    user = User.objects.get(username=request.user)

    following = Follow.objects.get(user=user).following.all()

    posts = Post.objects.filter(poster__in=following).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    num_pages = paginator.num_pages

    return render(request, "network/following.html", {
        'username': request.user,
        'page_obj': page_obj,
        'num_pages': range(1, num_pages + 1),
        'num_posts': posts.count(),
    })


@csrf_exempt
@login_required
def editpost(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "Request method must be PUT"}, status=404)

    user = User.objects.get(username=request.user)
    post = Post.objects.get(pk=id)
    new_content = json.loads(request.body).get('content')

    print(post.poster)
    if user != post.poster:
        return JsonResponse({"error": "You are not the creator of this post."}, status=404)
    
    post.content = new_content
    post.save()

    return JsonResponse({"message": "Post edited.", 'new_content': new_content}, status=201)


@csrf_exempt
@login_required
def like(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "Request method must be PUT"}, status=404)

    user = User.objects.get(username=request.user)
    post = Post.objects.get(pk=id)

    if user in post.likers.all():
        action = 'unliked'
        post.likers.remove(user)
    else:
        action = 'liked'
        post.likers.add(user)

    post.save()
    likescount = post.likers.count()
    return JsonResponse({"action": action, "likescount": likescount}, status=201)

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
            user_follow = Follow(user=user)
            user_follow.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
