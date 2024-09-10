from django import forms
from .models import Review

# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['rating', 'body']
#         widgets = {
#             'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
#             'body': forms.Textarea(attrs={'rows': 4}),
#         }

from django.core.exceptions import ValidationError
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'body']
    
    # def __init__(self, *args, **kwargs):
    #     self.product = kwargs.pop('product', None)
    #     super().__init__(*args, **kwargs)
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     if self.product and self.instance.user:
    #         # Check if the user has already reviewed the product
    #         if Review.objects.filter(product=self.product, user=self.instance.user).exists():
    #             raise ValidationError('You have already reviewed this product.')
    #     return cleaned_data