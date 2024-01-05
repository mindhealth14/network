from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import  PostSerializer
from network.models import Post
from rest_framework import status
from django.contrib import messages
from django.template.loader import get_template
# Create your views here.


@api_view(['GET'])
def postOverview(request):
    api_urls = {
        'List': '/post-list/',
        'Detail View': '/post-detail/<str:pk>/',
        'Create': '/post-create/',
        'Update': '/post-update/<int:pk>/',
        'Delete': '/post-delete/<str:pk>/',
    }

    return Response(api_urls)  # Return the API URLs as a dictionary



@api_view(['GET'])
def postList(request):
    posts = Post.objects.all().order_by('-id')
    serializer = PostSerializer(posts,  many = True)
    return Response(serializer.data)

@api_view(['GET'])
def postDetail(request, pk):
    posts = Post.objects.get(id=pk)
    serializer = PostSerializer(posts,  many = False)
    return Response(serializer.data)


@api_view(['POST'])
def postCreate(request):
    if request.user.is_authenticated:
        # Create a new Post instance with the author set to the authenticated user
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.save()
            # bring in the template to load
            post_template = get_template("network/post.html")
            post = Post.objects.get(id=serializer.data["id"])
            rendered_post = post_template.render({"post": post, "request": request})
            
            return HttpResponse(rendered_post, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['PUT'])
def postUpdate(request, pk): 
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
        
        update_text = request.data.get('text', "")
        if update_text !="":
            post.text = update_text
            post.save()
            return Response(serializer.data)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def postDelete(request, pk):
    try:
        post = Post.objects.get(id=pk)
        post.delete()
        return Response({"message": "Your post has been deleted."}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({"message": "The post does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": f"The post could not be deleted. Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    
    