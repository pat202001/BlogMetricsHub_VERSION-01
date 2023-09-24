from django import forms
from .models import Post,Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label=' ',widget=forms.TextInput(attrs={'placeholder' : 'Add  Your comment here....'}))

    class Meta:
        model = Comment
        fields = ('content',)


