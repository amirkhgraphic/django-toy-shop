from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.blog.models import Comment, Reply, Post


class RenderedForm(forms.ModelForm):
    submission_type = forms.CharField(widget=forms.HiddenInput(), initial='comment')
    comment = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].required = False

    class Meta:
        model = Comment
        fields = ('body', 'submission_type', 'comment')
        widgets = {
            'body': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='comment'
            )
        }


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].required = False

    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='comment'
            )
        }


class ReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].required = False

    class Meta:
        model = Reply
        fields = ('body',)
        widgets = {
            'body': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='comment'
            )
        }


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].required = False

    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'preview_body', 'body')
        widgets = {
            'body': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='extends'
            )
        }