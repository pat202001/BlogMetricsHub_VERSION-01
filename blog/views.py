from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.views import View
# from blog.forms import CommentForm
from django.forms import forms
from . models import Post,Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Comment
from PIL import Image
from .forms import CategoryForm, PostForm
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

# @login_required
# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html',context)
# @login_required

cats=Category.objects.all()
def CategoryViev(request,cats):
    category_posts=Post.objects.filter(category=cats)
    return render(request,'category_list.html',{'cats'})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

"""
Create a view function named 
view_category_posts
 that takes category_id as a parameter, 
retrieves the category and its associated 
posts, and renders a template to display those posts.
"""

def view_category_posts(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = category.posts.all()
    return render(request, 'blog/view_category_posts.html', {'category': category, 'posts': posts})


def about(request):
    return render(request, 'blog/about.html',{'title':"About Page"})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]
    """
    paginate here
    """
    paginate_by = 3

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post

    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data
"""
def get_context_data(self, *args ,**kwargs):
    cat_menu=Category.objects.all()
    context=super(PostDetailView,self).get_context_data(*args ,**kwargs)
    
    available_likes=get_object_or_404(Post,id=self.kwargs['pk'])
    total_likes=available_likes.total_likes() 
    liked=False
    if available_likes.likes.filter(id=self.request.user.id).exists():
        liked=True
        context["cat_menu"] =cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
    return context
"""

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by['-date_added']
    return render(request,'post_detail.html', {'post': post, 'comments': comments})

#    implementing  lik and unnlike using coolies sessions

def BlogPostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('blog-detail', args=[str(pk)]))


def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user if request.user.is_authenticated else None# Use authenticated user if available
        user_name = request.POST.get('user_name') if not request.user.is_authenticated else None
        if content:
            Comment.objects.create(post=post, content=content, user=user,user_name=user_name)
    return redirect('blog-detail', pk=post_id)



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # success_url = '/success/' 
    fields = ['title','categories', 'image_handler', 'content']

    def create_post(request,self):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.instance.author = self.request.user  # Assuming you have user authentication implemented
                post.save()
                form.save_m2m()  # Save the many-to-many relationships after saving the post
                return redirect('post_list')  # Redirect to the post list page
        else:
            form = PostForm()

        return render(request, 'create_post.html', {'form': form})


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'categories','image_handler','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

#  category
class CreateCategoryView(View):
    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        return render(request, 'add_category.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('category-list')  # Redirect to a success page or another appropriate page
        return render(request, 'add_category.html', {'form': form})
    
class  AddCategoryView(LoginRequiredMixin,CreateView):
    model=Category
    template_name = 'blog/add_category.html'
    fields = ['name']
    ordering = ["-created_at"]
    # fields='_all__'

def category_post_list(request, category_id):
    category = Category.objects.get(pk=category_id)
    posts = category.posts.all()  # Get all posts related to the selected category
    return render(request, 'category_post_list.html', {'category': category, 'posts': posts})