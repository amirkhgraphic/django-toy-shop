import os

from django_ckeditor_5.fields import CKEditor5Field

from django.db import models
from django.utils.translation import gettext_lazy as _

from shop.utils import product_path, brand_path, gallery_path
from utils.abstracts import User, MyBaseModel
from utils.mixins import GalleryMixin, CategoryMixin
from utils.utils import category_path, get_default_thumbnail, default_preview


class Brand(MyBaseModel):
    name = models.CharField(max_length=127, unique=True)
    thumbnail = models.ImageField(upload_to=brand_path, default='default/default.png')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.thumbnail and ('default' not in self.thumbnail.name):
            if os.path.isfile(self.thumbnail.path):
                os.remove(self.thumbnail.path)

        super().delete(*args, **kwargs)


class Product(MyBaseModel):
    title = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='brand_products', null=True, blank=True)
    preview_description = models.TextField(max_length=127, default=default_preview)
    description = CKEditor5Field(config_name='extends')
    quantity = models.PositiveIntegerField(default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_products')
    thumbnail = models.ImageField(upload_to=product_path, default='default/default.png')

    @property
    def latest_price(self):
        price_obj = self.prices.order_by('-created_at').first()
        if self.prices.exists():
            # return f'{price_obj.price} {price_obj.currency}'
            return price_obj.price
        return 0

    @property
    def is_available(self):
        return self.quantity > 0

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if 'default' not in self.thumbnail.name:
            Gallery.objects.get_or_create(file=self.thumbnail, product=self)

    def delete(self, *args, **kwargs):
        if self.thumbnail and ('default' not in self.thumbnail.name):
            if os.path.isfile(self.thumbnail.path):
                os.remove(self.thumbnail.path)

        super().delete(*args, **kwargs)


class Price(MyBaseModel):
    CURRENCY_CHOICES = (
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def get_latest_price(cls, instance):
        return cls.objects.filter(product=instance).first()


class Like(MyBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_likes')

    class Meta:
        unique_together = ('user', 'product')

    @classmethod
    def count_product_likes(cls, pk):
        return len(cls.objects.filter(product_id=pk))

    @classmethod
    def count_user_likes(cls, pk):
        return len(cls.objects.filter(user_id=pk))

    def __str__(self):
        return f'like #{self.id}'


class Category(MyBaseModel, CategoryMixin):
    thumbnail = models.ImageField(upload_to=category_path, default='default/default.png')

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class CategoryProduct(MyBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')

    def __str__(self):
        return f'{self.category.name}'


class Comment(MyBaseModel):
    body = CKEditor5Field(config_name='comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shop_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_comments')

    def __str__(self):
        return f'comment #{self.id}'


class Reply(MyBaseModel):
    body = CKEditor5Field(config_name='comment')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_replies')

    def __str__(self):
        return f'reply on {self.comment_id}'


class Gallery(MyBaseModel, GalleryMixin):
    file = models.FileField(upload_to=gallery_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media_files')

    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

    def delete(self, *args, **kwargs):
        if self.product.thumbnail == self.file:
            self.product.thumbnail = get_default_thumbnail()
            self.product.save()

        super().delete(*args, **kwargs)
