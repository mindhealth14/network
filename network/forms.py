from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:            
        model = Post
        fields = ('text',)
        widgets = {
    'text': forms.Textarea(
        
    attrs={
        'class': 'form-control js-post-text',
        'placeholder': "What's on your mind?",
        'rows': 3,
        'cols': 40,
        'data-post-url': 'your-post-url-value-here',
    }
)
        }       


class PostUpdateForm(forms.ModelForm):
    class Meta:            
        model = Post
        fields = ('text',)
        widgets = {
    'text': forms.Textarea(
        
    attrs={
        'class': 'form-control js-post-text',
        'placeholder': "What's on your mind?",
        'rows': 3,
        'cols': 40,
        'data-post-url': 'your-post-url-value-here',
    }
)
        }    