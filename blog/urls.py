from django.urls import path, include

from blog.views import (PostListView, PostCreateView, PostDetailView, CategoryListView, CategoryDetailView,
                        MyPostListView, PostUpdateView, PostDeleteView)


urlpatterns = [
    path('myposts/', MyPostListView.as_view(), name='my-posts'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('post/create/', PostCreateView.as_view(), name='create-post'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='update-post'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='delete-post'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category'),
]
