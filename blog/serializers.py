from rest_framework import serializers

from blog import User, Post, Like, Category, Comment, Gallery, CategoryPost


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'avatar')


class LikeSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()

    class Meta:
        model = Like
        fields = ('id', 'user')


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('id', 'file', 'post_id', 'format', 'type', 'created_at', 'updated_at')
        ordering = '-created_at'


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'body', 'parent_comment')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'thumbnail')


class CategoryPostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = CategoryPost
        fields = ('category',)


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    like_counts = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'thumbnail', 'title', 'body', 'author', 'like_counts', 'created_at', 'updated_at')

    def get_like_counts(self, post):
        return post.post_likes.count()


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    post_likes = LikeSerializer(many=True)
    media_files = GallerySerializer(many=True)
    post_comments = CommentSerializer(many=True)
    categories = CategoryPostSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'thumbnail', 'media_files', 'title', 'body', 'author', 'post_likes', 'post_comments',
                  'categories', 'created_at', 'updated_at')


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('thumbnail', 'title', 'author', 'preview_body', 'body')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('__all__')


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post', 'user')


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'thumbnail')


class GalleryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('file', 'post')
