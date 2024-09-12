from django import forms
from .models import Review, STAR_CHOICES  # Import STAR_CHOICES directly

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'body']
        widgets = {
            'rating': forms.Select(choices=STAR_CHOICES),
            'body': forms.Textarea(attrs={'rows': 4}),
        }
