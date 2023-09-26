from django.shortcuts import redirect, render
from django.http import HttpResponse
from blog.forms import CommentForm
from django.forms import forms
from . models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
# @login_required
# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html',context)
# @login_required
def about(request):
    return render(request, 'blog/about.html', {'title': "About Page"})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

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
    fields = ['title', 'content']

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
    
    
# comment form 
    def post_detail(request, pk):
        post = Post.objects.get(id=pk)
        if request.method == 'POST':
            c_form = CommentForm(request.POST)
            if c_form.is_valid():
                instance = c_form.save(commit=False)
                instance.user = request.user
                instance.post = post
                instance.save()
                return redirect('blog-detail', pk=post.id)
        else:
            c_form = CommentForm()
        context = {
            'post': post,
            'c_form': c_form,
        }
        return render(request, 'blog/post_detail.html', context)
