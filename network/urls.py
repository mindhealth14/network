
from django.urls import path

from . import views

urlpatterns = [
    path("", views.feed, name="index"),
    path("mypost", views.my_post, name="my_post"),
    path("new/", views.CreateNewPost.as_view(), name="new_post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("likes/<int:post_id>/", views.post_likes, name="likes"),
    path("like_count/<int:post_id>/", views.like_count, name="like_count"),
    path("following_post", views.following_post, name="follow_post"),
    path("post_details/<int:post_id>", views.post_details, name="post_details"),

]
