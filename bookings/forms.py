from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking, Payment
from destinations.models import Accommodation, Activity

class BookingForm(forms.ModelForm):
    activities = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Booking
        fields = ['accommodation', 'start_date', 'end_date', 'adults', 'children', 'special_requests']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'adults': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'children': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        destination = kwargs.pop('destination', None)
        super().__init__(*args, **kwargs)
        
        if destination:
            # Filter accommodations by destination
            self.fields['accommodation'].queryset = Accommodation.objects.filter(destination=destination)
            self.fields['accommodation'].widget.attrs.update({'class': 'form-control'})
            
            # Filter activities by destination
            self.fields['activities'].queryset = Activity.objects.filter(destination=destination)
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        # Check if dates are in the future
        if start_date and start_date < timezone.now().date():
            raise ValidationError('Start date must be in the future.')
        
        # Check if end date is after start date
        if start_date and end_date and end_date <= start_date:
            raise ValidationError('End date must be after start date.')
        
        # Check if booking is at least 1 day
        if start_date and end_date and (end_date - start_date).days < 1:
            raise ValidationError('Booking must be at least 1 day.')
        
        return cleaned_data

class PaymentForm(forms.ModelForm):
    card_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'})
    )
    card_holder = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Holder Name'})
    )
    expiry_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'})
    )
    cvv = forms.CharField(
        max_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'})
    )
    
    class Meta:
        model = Payment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not card_number.isdigit():
            raise ValidationError('Card number must contain only digits.')
        if len(card_number) != 16:
            raise ValidationError('Card number must be 16 digits.')
        return card_number
    
    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if not expiry_date or len(expiry_date) != 5 or expiry_date[2] != '/':
            raise ValidationError('Expiry date must be in the format MM/YY.')
        
        try:
            month = int(expiry_date[:2])
            year = int(expiry_date[3:])
            
            if month < 1 or month > 12:
                raise ValidationError('Invalid month in expiry date.')
            
            current_year = timezone.now().year % 100
            if year < current_year:
                raise ValidationError('Card has expired.')
            
            if year == current_year and month < timezone.now().month:
                raise ValidationError('Card has expired.')
        except ValueError:
            raise ValidationError('Invalid expiry date format.')
        
        return expiry_date
    
    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if not cvv.isdigit():
            raise ValidationError('CVV must contain only digits.')
        if len(cvv) != 3:
            raise ValidationError('CVV must be 3 digits.')
        return cvv
