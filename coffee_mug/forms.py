from django.forms import ModelForm
from django import forms
from . models import ProductReview


class ProductReviewForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'name': 'product-review',
        'id': 'product-review',
        'row': 5
    }))

    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']