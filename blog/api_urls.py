from django.urls import path

from blog.api import (PostListAPIView, PostDetailAPIView, PostCreateAPIView, PostRetrieveUpdateAPIView,
                      PostRetrieveDestroyAPIView, CommentCreateAPIView, CommentListAPIView,
                      CommentRetrieveAPIView, CommentDestroyAPIView, CommentUpdateAPIView, like_api_view,
                      CategoryCreateAPIView, GalleryCreateAPIView, CategoryPostDeleteAPIView,
                      GalleryDeleteAPIView)


urlpatterns = [
    # Post API
    path('post/list/', PostListAPIView.as_view(), name='list-post'),
    path('post/create/', PostCreateAPIView.as_view(), name='create-post'),
    path('post/retrieve/<int:pk>', PostDetailAPIView.as_view(), name='retrieve-post'),
    path('post/update/<int:pk>', PostRetrieveUpdateAPIView.as_view(), name='update-post'),
    path('post/delete/<int:pk>', PostRetrieveDestroyAPIView.as_view(), name='delete-post'),

    # Comment API
    path('comment/list/', CommentListAPIView.as_view(), name='list-comment'),
    path('comment/create/', CommentCreateAPIView.as_view(), name='create-comment'),
    path('comment/retrieve/<int:pk>', CommentRetrieveAPIView.as_view(), name='retrieve-comment'),
    path('comment/update/<int:pk>', CommentUpdateAPIView.as_view(), name='update-comment'),
    path('comment/delete/<int:pk>', CommentDestroyAPIView.as_view(), name='delete-comment'),

    # Like API
    path('like/<int:post_id>/<int:user_id>/', like_api_view, name='like'),

    # Category API
    path('category/create/', CategoryCreateAPIView.as_view(), name='create-category'),
    path('category/delete/', CategoryPostDeleteAPIView.as_view(), name='delete-category'),

    # Gallery API
    path('gallery/create/', GalleryCreateAPIView.as_view(), name='create-gallery'),
    path('gallery/delete/<int:pk>/', GalleryDeleteAPIView.as_view(), name='delete-gallery'),
]
