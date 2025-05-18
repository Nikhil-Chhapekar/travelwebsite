from django import forms
from .models import Review, AccommodationReview, ActivityReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating', 'visit_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class AccommodationReviewForm(forms.ModelForm):
    class Meta:
        model = AccommodationReview
        fields = ['title', 'content', 'rating', 'stay_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'stay_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class ActivityReviewForm(forms.ModelForm):
    class Meta:
        model = ActivityReview
        fields = ['title', 'content', 'rating', 'activity_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'activity_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
