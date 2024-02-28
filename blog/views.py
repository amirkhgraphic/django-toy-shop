from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import CommentForm, RenderedForm, ReplyForm, PostForm
from blog.models import Post, Like, Category, CategoryPost


@method_decorator(login_required, name='dispatch')
class MyPostListView(ListView):
    model = Post
    template_name = 'blog/my-posts.html'
    context_object_name = 'posts'
    ordering = ('-created_at', '-updated_at')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class PostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    ordering = ('-created_at', '-updated_at')


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create-post.html'
    success_url = reverse_lazy('blog:posts')

    def form_valid(self, form):
        form.instance.author = self.request.user

        post = form.save()

        selected_categories = set(self.request.POST.getlist('category-id'))

        for category_id in selected_categories:
            CategoryPost.objects.get_or_create(post=post, category_id=category_id)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/update-post.html'

    def get_success_url(self):
        return reverse_lazy('blog:post', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        post = form.save()

        selected_categories = set(self.request.POST.getlist('category-id'))

        for category_id in selected_categories:
            CategoryPost.objects.get_or_create(post=post, category_id=category_id)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/delete-post.html'
    success_url = reverse_lazy('blog:my-posts')

    def get_success_url(self):
        return self.success_url

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author == self.request.user:
            self.object.delete()

        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user if self.request.user.is_authenticated else None
        context['recent_posts'] = Post.objects.order_by('-created_at')[:5]
        context['liked_users'] = Like.objects.filter(post=self.object).values_list('user_id', flat=True)
        context['form'] = RenderedForm()

        comments = self.object.post_comments.count()
        replies = sum(comment.replies.count() for comment in self.object.post_comments.all())
        context['comments_count'] = comments + replies

        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
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
                            comment.post = post
                            comment.save()
                    return redirect(reverse_lazy('blog:post', args=[post.id]))
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
                    return redirect(reverse_lazy('blog:post', args=[post.id]))
                else:
                    context = self.get_context_data(**kwargs)
                    return self.render_to_response(context)


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/categories.html'
    context_object_name = 'categories'
    ordering = ('-created_at', '-updated_at')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'category'
