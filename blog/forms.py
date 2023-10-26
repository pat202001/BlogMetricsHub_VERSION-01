from django import forms
from .models import Post, Comment,Category

"""
choices=Category.objects.all().values_list('name','name')
choices_list=[]
for item in choices:
    choices_list.append(item)

class PostForm(forms.ModelForm):
           widget={
       'title': forms.TextInput(attrs={'class':'form-control'}),
        'content': forms.Textarea(attrs={'class':'form-control'}),
         'category': forms.Select(attrs={'class':'form-control'})

          } 
        """
"""
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']  # Include 'categories' field in the form

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
"""
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'categories', 'content', 'image_handler']  # Include 'category' field in the form
def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['categories'].required = True 
        
    # Add a widget to display categories as checkboxes
category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),  # Assuming Category is the model for categories
        widget=forms.CheckboxSelectMultiple
    )


from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)  # Fields you want to include in your form




class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','categories','image_handler','content')

"""
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='', widget=forms.Textarea(attrs={'placeholder': 'Add comment here....'}))

    class Meta:
        model = Comment
        fields = ('user_name', 'content',)
"""

