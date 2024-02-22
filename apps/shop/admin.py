from django.contrib import admin

from apps.shop.models import Category, Product, Comment, Gallery, CategoryProduct, Brand, Price, Reply
from utils.admin.mixins import ThumbnailMixin, RenderContentMixin, ActionsMixin, InlineMixin, \
    DateListFilterMixin, LinkifyMixin


class CategoryProductInline(InlineMixin, admin.TabularInline):
    model = CategoryProduct


class CommentInline(InlineMixin, admin.StackedInline):
    model = Comment


class ReplyInline(InlineMixin, admin.StackedInline):
    model = Reply


class GalleryInline(InlineMixin, RenderContentMixin, admin.TabularInline):
    model = Gallery

    readonly_fields = InlineMixin.readonly_fields + ('render_content', 'render_name')


class PriceInline(InlineMixin, admin.TabularInline):
    model = Price


@admin.register(Category)
class CategoryAdmin(DateListFilterMixin, ActionsMixin, ThumbnailMixin, admin.ModelAdmin):
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


@admin.register(Product)
class ProductAdmin(DateListFilterMixin, LinkifyMixin, ActionsMixin, ThumbnailMixin, admin.ModelAdmin):
    list_display = ('render_thumbnail', 'title', 'brand', 'seller_link', 'latest_price', 'is_available', 'quantity',
                    'created_at', 'updated_at', 'is_active')
    list_filter = ('brand', 'seller', 'categories') + DateListFilterMixin.list_filter
    fields = ('title', ('thumbnail', 'render_thumbnail'), 'brand', 'quantity', 'preview_description', 'description',
              'seller', 'created_at', 'updated_at')
    inlines = (PriceInline, CategoryProductInline, CommentInline, GalleryInline)
    readonly_fields = ('render_thumbnail', 'created_at', 'is_available', 'updated_at')
    search_fields = ('title', 'description', 'quantity')
    ordering = ('-created_at', '-updated_at', '-quantity')

    actions = ('activate_objects', 'deactivate_objects')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)

    def is_available(self, obj):
        return obj.quantity > 0

    is_available.boolean = True
    is_available.short_description = 'Available'


@admin.register(Brand)
class BrandAdmin(DateListFilterMixin, ActionsMixin, ThumbnailMixin, admin.ModelAdmin):
    list_display = ('render_thumbnail', 'name', 'created_at', 'updated_at', 'is_active')
    fields = ('name', ('thumbnail', 'render_thumbnail'), 'created_at', 'updated_at', 'is_active')
    readonly_fields = ('render_thumbnail', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at', '-updated_at')

    actions = ('activate_objects', 'deactivate_objects')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)


@admin.register(Comment)
class CommentAdmin(DateListFilterMixin, LinkifyMixin, ActionsMixin, admin.ModelAdmin):
    list_display = ('__str__', 'author_link', 'product_link', 'created_at', 'updated_at', 'is_active')
    list_filter = ('author', 'product') + DateListFilterMixin.list_filter
    fields = ('author', 'product', 'body', 'created_at', 'updated_at', 'is_active')
    inlines = (ReplyInline,)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('body',)
    ordering = ('-created_at', '-updated_at')

    actions = ('activate_objects', 'deactivate_objects')


@admin.register(Gallery)
class GalleryAdmin(DateListFilterMixin, LinkifyMixin, ActionsMixin, RenderContentMixin, admin.ModelAdmin):
    list_display = ('render_content_small', 'render_name', 'product_link', 'type', 'format', 'created_at', 'is_active')
    list_filter = ('type', 'format', 'product') + DateListFilterMixin.list_filter
    fields = ('render_content', 'file', 'product', 'type', 'format', 'created_at', 'updated_at')
    readonly_fields = ('render_content', 'render_name', 'type', 'format', 'created_at', 'updated_at')
    ordering = ('-created_at', '-updated_at')

    actions = ('activate_objects', 'deactivate_objects')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)
