import os

from django_ckeditor_5.fields import CKEditor5Field

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.blog.utils import post_path, gallery_path
from utils.abstracts import User, MyBaseModel
from utils.mixins import GalleryMixin, CategoryMixin
from utils.utils import category_path, get_default_thumbnail, default_preview


class Post(MyBaseModel):
    title = models.CharField(max_length=255)
    preview_body = models.TextField(max_length=127, default=default_preview)
    body = CKEditor5Field(config_name='extends')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_posts')
    thumbnail = models.ImageField(upload_to=post_path, default='default/default.png')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if 'default' not in self.thumbnail.name:
            Gallery.objects.get_or_create(file=self.thumbnail, post=self)

    def delete(self, *args, **kwargs):
        if self.thumbnail and ('default' not in self.thumbnail.name):
            if os.path.isfile(self.thumbnail.path):
                os.remove(self.thumbnail.path)

        super().delete(*args, **kwargs)


class Category(MyBaseModel, CategoryMixin):
    thumbnail = models.ImageField(upload_to=category_path, default='default/default.png')

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class CategoryPost(MyBaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')

    def __str__(self):
        return f'{self.category.name}'


class Like(MyBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    class Meta:
        unique_together = ('user', 'post')

    @classmethod
    def count_post_likes(cls, pk):
        return len(cls.objects.filter(post_id=pk))

    @classmethod
    def count_user_likes(cls, pk):
        return len(cls.objects.filter(user_id=pk))

    def __str__(self):
        return f'like #{self.id}'


class Comment(MyBaseModel):
    body = CKEditor5Field(config_name='comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')

    def __str__(self):
        return f'comment #{self.id}'


class Reply(MyBaseModel):
    body = CKEditor5Field(config_name='comment')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_replies')

    def __str__(self):
        return f'reply on {self.comment_id}'


class Gallery(MyBaseModel, GalleryMixin):
    file = models.FileField(upload_to=gallery_path)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media_files')

    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

    def delete(self, *args, **kwargs):
        if self.post.thumbnail == self.file:
            self.post.thumbnail = get_default_thumbnail()
            self.post.save()

        super().delete(*args, **kwargs)
