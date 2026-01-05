from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Tweet, Follow, Like
from django.core.cache import cache
import os
from .models import *

MAX_ATTEMPTS = 5
BLOCK_TIME = 15 * 60

def register_view(request):
    if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']

         if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
            return redirect('register')

         User.objects.create_user(
            username=username,
            password=password
        )
         messages.success(request, 'Account created successfully. Please log in.')
         return redirect('login')
    return render(request, 'register.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def login_view(request):

     ip = get_client_ip(request)
     cache_key = f'login_attempts_{ip}'
     attempts = cache.get(cache_key, 0)

     if attempts >= MAX_ATTEMPTS:
        messages.error(
            request,
            'Too many failed login attempts. Try again later.'
        )
        return render(request, 'login.html')


     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            cache.delete(cache_key)
            login(request, user)
            return redirect('home')
        else:
            cache.set(
                cache_key,
                attempts + 1,
                timeout=BLOCK_TIME
            )
            remaining = MAX_ATTEMPTS - (attempts + 1)
            messages.error(request,  f'Invalid credentials. {remaining} attempts remaining.')
            return redirect('login')

     return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        files = request.FILES.getlist('attachment')


        allowed_extensions = [
            '.jpg', '.jpeg', '.png', '.gif',
            '.mp4',
            '.mp3',
            '.pdf', '.docx', '.xlsx'
        ]

        MAX_FILE_SIZE = 10 * 1024 * 1024  #10MB limit


        for file in files:
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in allowed_extensions:
                messages.error(request, 'Unsupported file type')
                return redirect('home')
            
            if file.size > MAX_FILE_SIZE:
                messages.error(
                request,
                f'File too large (max 10MB): {file.name}'
            )
            
        if not content and (not files or files.size ==0):
            messages.error(request, 'You must provide either text content or a file.')
            return redirect('home')

        post = Tweet.objects.create(
            user=request.user,
            content=content
        )

        for file in files:
            Attachment.objects.create(
            post=post,
            file=file
        )


        return redirect('home')
        
    following = Follow.objects.filter(
        follower=request.user
    ).values_list('following', flat=True)

    tweets = Tweet.objects.filter(
        user__in=list(following) + [request.user]
    ).order_by('-created_at')

    return render(request, 'home.html', {'tweets': tweets})

@login_required
def delete_tweet(request,tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    if tweet.user ==request.user:

        if tweet.attachment:
            tweet.attachment.delete(save=False)

        tweet.delete()
        messages.success(request, 'Tweet deleted successfully')
    else:
        messages.error(request, 'You do not have permission to delete this.')

    return redirect('home')

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)

    followers_count = Follow.objects.filter(
        following=user
    ).count()

    following_count = Follow.objects.filter(
        follower=user
    ).count()

    tweets = Tweet.objects.filter(user=user)
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, 'profile.html', {
        'profile_user': user,
        'tweets': tweets,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    })

@login_required
def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    Follow.objects.get_or_create(follower=request.user, following=user)
    return redirect('profile', username=username)

def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)
    Follow.objects.filter(
        follower=request.user,
        following=user
    ).delete()
    return redirect('profile', username=username)

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    Like.objects.get_or_create(user=request.user, tweet=tweet)
    return redirect('home')
