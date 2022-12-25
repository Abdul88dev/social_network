from django import forms
from .models import Post

#strip to remove empty spaces
class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)

class CreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text','main_img']  # Picture is manual