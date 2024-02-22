from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from apps.shop.forms import RenderedForm, CommentForm, ReplyForm, ProductForm
from apps.shop.models import Product, Like, CategoryProduct, Price, Brand, Category


class ProductListView(ListView):
    queryset = Product.objects.filter(is_active=True)
    template_name = 'shop/shop.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'shop/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user if self.request.user.is_authenticated else None
        context['recent_products'] = Product.objects.order_by('-created_at')[:3]
        context['liked_users'] = Like.objects.filter(product=self.object).values_list('user_id', flat=True)
        context['form'] = RenderedForm()

        comments = self.object.shop_comments.count()
        replies = sum(comment.replies.count() for comment in self.object.shop_comments.all())
        context['comments_count'] = comments + replies

        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = RenderedForm(request.POST)
        if form.is_valid():
            comment_id = form.cleaned_data['comment']
            if form.cleaned_data['submission_type'] == 'comment':
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    if comment:
                        if comment.body:
                            comment.author = request.user
                            comment.product = product
                            comment.save()
                    return redirect(reverse_lazy('shop:product', args=[product.id]))
                else:
                    context = self.get_context_data(**kwargs)
                    return self.render_to_response(context)
            else:
                form = ReplyForm(request.POST)
                if form.is_valid():
                    reply = form.save(commit=False)
                    if reply:
                        if reply.body:
                            reply.author = request.user
                            reply.comment_id = comment_id
                            reply.save()
                    return redirect(reverse_lazy('shop:product', args=[product.id]))
                else:
                    context = self.get_context_data(**kwargs)
                    return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
class MyProductsListView(ListView):
    model = Product
    template_name = 'shop/my-products.html'
    context_object_name = 'products'
    ordering = ('-created_at', '-updated_at')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(seller=self.request.user)


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/create-product.html'
    success_url = reverse_lazy('shop:my-products')

    def form_valid(self, form):
        form.instance.seller = self.request.user

        product = form.save(commit=False)

        brand_name = form.cleaned_data['new_brand']
        if brand_name:
            brand, created = Brand.objects.get_or_create(name=brand_name)
            product.brand = brand
        product.save()

        selected_categories = set(self.request.POST.getlist('category-id'))

        for category_id in selected_categories:
            CategoryProduct.objects.get_or_create(product=product, category_id=category_id)

        price = self.request.POST.get('price')
        currency = self.request.POST.get('currency')

        if price and currency:
            Price.objects.get_or_create(price=price, currency=currency, product=product)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/update-product.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse_lazy('shop:product', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        product = form.save(commit=False)

        brand_name = form.cleaned_data['new_brand']
        if brand_name:
            brand, created = Brand.objects.get_or_create(name=brand_name)
            product.brand = brand
        product.save()

        selected_categories = set(self.request.POST.getlist('category-id'))

        for category_id in selected_categories:
            CategoryProduct.objects.get_or_create(product=product, category_id=category_id)

        price = self.request.POST.get('price')
        currency = self.request.POST.get('currency')
        latest_price = Price.get_latest_price(product)

        if (price is not None) and (currency is not None) and ((int(price) != int(latest_price.price)) or
                                                               (latest_price.currency != currency)):
            Price.objects.create(price=price, currency=currency, product=product)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/delete-product.html'
    success_url = reverse_lazy('shop:my-products')

    def get_success_url(self):
        return self.success_url

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.seller == self.request.user:
            self.object.delete()

        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/categories.html'
    context_object_name = 'categories'
    ordering = ('-created_at', '-updated_at')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category.html'
    context_object_name = 'category'


class BrandListView(ListView):
    model = Brand
    template_name = 'shop/brands.html'
    context_object_name = 'brands'
    ordering = ('-created_at', '-updated_at')


class BrandDetailView(DetailView):
    model = Brand
    template_name = 'shop/brand.html'
    context_object_name = 'brand'

