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
    
    def clean(self):
        cleaned_data = super().clean()
        product = self.instance.product
        user = self.instance.user
        
        # Check if the user has already reviewed the product
        if Review.objects.filter(product=product, user=user).exists():
            raise ValidationError('You have already reviewed this product.')

        return cleaned_data
