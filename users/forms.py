from django import forms
from store.models import BillingDetail


class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingDetail
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'billing-input w-input', 'maxlength': '256', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'billing-input w-input', 'maxlength': '256', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'billing-input w-input', 'maxlength': '256', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'billing-input w-input', 'maxlength': '256', 'placeholder': 'Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'billing-input w-input', 'maxlength': '256', 'placeholder': 'Enter Home Address'}),            
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = False