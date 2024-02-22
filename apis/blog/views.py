from apis.blog.serializers import (PostListSerializer, PostDetailSerializer, PostCreateSerializer,
                                   CommentCreateSerializer, LikeCreateSerializer, CategoryCreateSerializer,
                                   GallerySerializer)
from rest_framework.generics import (ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView, DestroyAPIView)
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.blog.models import Post, Comment, Like, Category, Gallery, CategoryPost


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().order_by('-created_at', '-updated_at')
    serializer_class = PostListSerializer


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all().order_by('-created_at', '-updated_at')
    serializer_class = PostDetailSerializer


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer


class CommentRetrieveAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer


class CommentUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer


class CommentDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer


@api_view(['POST'])
def like_api_view(request, post_id, user_id):
    try:
        like = Like.objects.get(post_id=post_id, user_id=user_id)
        like.delete()  # Remove like if it already exists
        return Response({'detail': 'removed'}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        # Like does not exist, so create it
        like_data = {'post': post_id, 'user': user_id}
        serializer = LikeCreateSerializer(data=like_data)
        if serializer.is_valid():
            Like.objects.create(post_id=post_id, user_id=user_id)
            return Response({'detail': 'created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    def create(self, request, *args, **kwargs):
        category_name = request.data.get('name')
        existing_category = Category.objects.filter(name__iexact=category_name).first()

        if existing_category:
            serializer = self.get_serializer(existing_category)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class GalleryCreateAPIView(CreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        post_id = self.request.data.get('post_id')
        serializer.save(post_id=post_id)


class CategoryPostDeleteAPIView(APIView):
    def delete(self, request):
        post_id = request.query_params.get('post_id')
        category_id = request.query_params.get('category_id')

        if post_id is None or category_id is None:
            return Response({'error': 'post_id and category_id are required in query parameters'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            category_post = CategoryPost.objects.get(post_id=post_id, category_id=category_id)
            category_post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CategoryPost.DoesNotExist:
            return Response({'error': 'CategoryPost does not exist'}, status=status.HTTP_404_NOT_FOUND)


class GalleryDeleteAPIView(DestroyAPIView):
    queryset = Gallery.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
