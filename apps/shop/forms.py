from django_ckeditor_5.widgets import CKEditor5Widget

from django import forms

from apps.shop.models import Comment, Reply, Product, Price


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


class ProductForm(forms.ModelForm):
    price = forms.IntegerField()
    currency = forms.ChoiceField(choices=Price.CURRENCY_CHOICES)
    new_brand = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['new_brand'].required = False

        instance = kwargs.get('instance')
        price = Price.get_latest_price(instance)
        if instance:
            self.fields['price'].initial = price.price
            self.fields['currency'].initial = price.currency

    class Meta:
        model = Product
        fields = ('title', 'thumbnail', 'brand', 'new_brand', 'preview_description', 'description', 'quantity', 'price', 'currency')
        widgets = {
            'description': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='extends'
            )
        }
