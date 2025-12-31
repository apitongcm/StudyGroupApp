from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>/', profile, name='profile'),
    path('follow/<str:username>/', follow_user, name='follow'),
    path('like/<int:tweet_id>/', like_tweet, name='like'),
]
