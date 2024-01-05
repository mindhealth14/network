from django.urls import path
from . import views 
from .views import UserFollowView


urlpatterns = [
    # ... other URL patterns ...
    path('profile/<str:username>/', views.profile_detail, name='profile-detail'),
     path("<str:username>/follow/", UserFollowView.as_view(), name="user_follow"),
     path("like_counts/<int:post_id>/", views.like_counts, name="like_counts"),
]