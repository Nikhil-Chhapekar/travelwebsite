from django import forms
from .models import AccommodationBooking

class AccommodationBookingForm(forms.ModelForm):
    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control date-picker'})
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control date-picker'})
    )
    special_requests = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=False
    )
    
    class Meta:
        model = AccommodationBooking
        fields = [
            'full_name', 'email', 'phone', 'check_in_date', 'check_out_date', 
            'room_type', 'guests', 'special_requests'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'guests': forms.Select(attrs={
                'class': 'form-select',
                'choices': [(i, f"{i} Guest{'s' if i > 1 else ''}") for i in range(1, 5)]
            }),
        }
