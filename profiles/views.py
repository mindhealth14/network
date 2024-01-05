from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from network.models import Post
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from followers.models import Follower



# Create your views here.


def profile_detail(request, username):
     User = get_user_model()
     user = User.objects.get(username=username)
    
     de_post = Post.objects.filter(author=user).order_by('-id')[0:10]
    
     if request.user.is_authenticated:
      you_follow = Follower.objects.filter(following=user, followed_by=request.user).exists()


     return render(request, 'network/profile_detail.html', {
         
         'user': user,
         'you_follow': you_follow,
         'de_post': de_post,
         
         })
    

# Like Count
def like_counts(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=post_id )
        like_count = post.likes.count()  # Changed variable name to snake_case
        return JsonResponse({'likeCounts': like_count})
    
    

class UserFollowView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        User = get_user_model()

        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest()  

        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})

        if data['action'] == "follow":
            # Follow
            follower, created = Follower.objects.get_or_create(
                followed_by=request.user,
                following=other_user
            )
            wording = "Unfollow"  # You followed the user, so the wording should be "Unfollow"
            total_followers = Follower.objects.filter(following=other_user).count()
            
        else:
            # Unfollow
            follower = Follower.objects.filter(
                followed_by=request.user,
                following=other_user
            ).first()
            if follower:
                follower.delete()
            wording = "Follow"  # You unfollowed the user, so the wording should be "Follow"
            total_followers = Follower.objects.filter(following=other_user).count()
            

        return JsonResponse({
            'success': True,
            'wording': wording,
            'total_followers': total_followers
        })
    


    