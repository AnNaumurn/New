from django import forms
from .models import User_posts

class UserPostsForm(forms.ModelForm):
    class Meta:
        model = User_posts
        fields = ['post']