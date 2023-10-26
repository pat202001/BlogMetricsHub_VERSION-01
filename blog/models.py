from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms import forms
from django.urls import reverse
from PIL import Image
from ckeditor.fields import RichTextField
# from .models import Category

# Create your models here
class Category(models.Model): 
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})
    
    """
    class Post(models.Model):
    title = models.CharField(max_length=200)
    content=RichTextField(null=True,blank=True)
    image_handler=models.ImageField(null=True,blank=True ,upload_to="images/")
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)
    category = models.ManyToManyField(Category,default='coding', related_name='posts',blank=True)
    """
class Post(models.Model):
    title = models.CharField(max_length=200)
    content=RichTextField(null=True,blank=True)
    image_handler=models.ImageField(null=True,blank=True ,upload_to="images/")
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    
    def __str__(self):
        return self.title
    
    def number_of_likes(self):
        return self.likes.count()
    
    # other fields like author, date_posted, etc.

    """
        def total_likes(self):
                
                return self.likes.count()
    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image_handler.path)
        if img.height >= 700 or img.width >= 700:
            output_size = (600, 800)
            img.thumbnail(output_size)
            img.save(self.image_handler.path)

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})
    
    def comment_count(self):
        return self.comment_set.all().count()

    def comments(self):
        return self.comment_set.all()

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=255, null=True, blank=True)
    content = models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)

def __str__(self):
        return  '%s - %s' % (self.post.title,self.name)
 
  

