from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,BlogPostLike,AddCategoryView,CreateCategoryView

urlpatterns=[
    # path('', views.home,name='blog-hame'),
    path('about/', views.about,name='blog-about'),
    # path('contact/', views.contact,name='blog-contact'),
   path('', PostListView.as_view(), name="blog-home"),
    path('post-new/', PostCreateView.as_view(), name="blog-new"),
    path('add_category/',AddCategoryView.as_view(), name='add_category'),
    path('create_category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('category_list/', views.category_list, name='category-list'),
     path('post/<int:pk>/', views.PostDetailView.as_view(), name='blog-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="blog-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="blog-delete"),
     path('post/<int:post_id>/comment/', views.comment_post, name='comment_post'),
    # path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    # path('like/<int:pk>',LikeView,name='like_post'),
    # path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    #  path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    # path('like/<str:post_id>/', views.LikeView, name='like_post'),
    # path('post/create/', views.create_post, name='create_post'),

    #     displaying  all posts in this category
     path('blogpost-like/<int:pk>', views.BlogPostLike, name="blogpost_like"),
   
    path('category/<int:category_id>/', views.view_category_posts, name='view_category_posts'),

    
  

]   