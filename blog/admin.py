from django.contrib import admin
from django.db.models import Count

from blog.models import Category, Post, Comment, Gallery, CategoryPost, Like, Reply
from utils.admin.mixins import (ThumbnailMixin, RenderContentMixin, ActionsMixin, InlineMixin, LinkifyMixin,
                                DateListFilterMixin)


class CategoryPostInline(InlineMixin, admin.TabularInline):
    model = CategoryPost


class LikeInline(InlineMixin, admin.TabularInline):
    model = Like


class CommentInline(InlineMixin, admin.StackedInline):
    model = Comment


class ReplyInline(InlineMixin, admin.StackedInline):
    model = Reply


class GalleryInline(RenderContentMixin, InlineMixin, admin.TabularInline):
    model = Gallery

    readonly_fields = InlineMixin.readonly_fields + ('render_content', 'render_name')


class CategoryFilter(admin.SimpleListFilter):
    title = 'Categories'
    parameter_name = 'categories'

    def lookups(self, request, model_admin):
        categories = Category.objects.all().order_by('name')
        return [(category.id, category.name) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            category_id = self.value()
            posts_ids = CategoryPost.objects.filter(category_id=category_id).values_list('post_id', flat=True)
            return queryset.filter(id__in=posts_ids)
        return queryset


@admin.register(Post)
class PostAdmin(LinkifyMixin, DateListFilterMixin, ActionsMixin, ThumbnailMixin, admin.ModelAdmin):
    list_display = ('render_thumbnail', 'title', 'author_link', 'likes_count', 'created_at', 'updated_at', 'is_active')
    list_filter = ('author', CategoryFilter) + DateListFilterMixin.list_filter
    fields = ('title', ('thumbnail', 'render_thumbnail'), 'body', 'author', 'likes_count', 'created_at', 'updated_at')
    inlines = (LikeInline, CategoryPostInline, CommentInline, GalleryInline)
    readonly_fields = ('render_thumbnail', 'likes_count', 'created_at', 'updated_at')
    search_fields = ('title', 'body')
    ordering = ('-created_at', '-updated_at')

    actions = ('activate_objects', 'deactivate_objects')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(num_likes=Count('post_likes'))
        return queryset

    def likes_count(self, obj):
        return obj.num_likes

    likes_count.short_description = 'Likes'


@admin.register(Category)
class CategoryAdmin(DateListFilterMixin, ActionsMixin, ThumbnailMixin, admin.ModelAdmin):
    inlines = [CategoryPostInline]
    list_display = ('render_thumbnail', 'name', 'created_at', 'updated_at', 'is_active')
    fields = ('name', 'thumbnail', 'render_thumbnail', 'created_at', 'updated_at')
    readonly_fields = ('render_thumbnail', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at', '-updated_at')

    actions = ('activate_objects', 'deactivate_objects')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)


@admin.register(Like)
class LikeAdmin(LinkifyMixin, ActionsMixin, DateListFilterMixin, admin.ModelAdmin):
    list_display = ('__str__', 'user_link', 'post_link', 'created_at', 'updated_at', 'is_active')
    list_filter = ('user', 'post') + DateListFilterMixin.list_filter
    fields = ('user', 'post')
    readonly_fields = ('created_at', 'updated_at', 'is_active')
    ordering = ('-created_at', '-updated_at')

    actions = ('activate_objects', 'deactivate_objects')


@admin.register(Comment)
class CommentAdmin(LinkifyMixin, DateListFilterMixin, ActionsMixin, admin.ModelAdmin):
    list_display = ('__str__', 'author_link', 'post_link', 'created_at', 'updated_at', 'is_active')
    list_filter = ('author', 'post') + DateListFilterMixin.list_filter
    fields = ('author', 'post', 'body', 'created_at', 'updated_at', 'is_active')
    inlines = (ReplyInline,)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('body',)
    ordering = ('-created_at', '-updated_at')

    actions = ('activate_objects', 'deactivate_objects')


@admin.register(Reply)
class ReplyAdmin(LinkifyMixin, DateListFilterMixin, ActionsMixin, admin.ModelAdmin):
    list_display = ('__str__', 'author_link', 'comment_link', 'created_at', 'updated_at', 'is_active')
    list_filter = ('author', 'comment') + DateListFilterMixin.list_filter
    fields = ('author', 'comment', 'body', 'created_at', 'updated_at', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('body',)
    ordering = ('-created_at', '-updated_at')

    actions = ('activate_objects', 'deactivate_objects')


@admin.register(Gallery)
class GalleryAdmin(LinkifyMixin, DateListFilterMixin, ActionsMixin, RenderContentMixin, admin.ModelAdmin):
    list_display = ('render_content_small', 'post_link', 'type', 'format', 'created_at', 'is_active')
    list_filter = ('type', 'format', 'post') + DateListFilterMixin.list_filter
    fields = ('render_content', 'render_name', 'file', 'type', 'format', 'post', 'created_at', 'updated_at')
    readonly_fields = ('render_content', 'render_name', 'type', 'format', 'created_at', 'updated_at')
    ordering = ('-created_at', '-updated_at')

    actions = ('activate_objects', 'deactivate_objects')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)
