# solo_project_app/forms.py

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description']  # Add any other fields you need in the form
