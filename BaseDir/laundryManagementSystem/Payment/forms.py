from .models import Payment
from django import forms



class PaymentForm(forms.ModelForm):
    """Form definition for Payment."""

    class Meta:
        """Meta definition for Paymentform."""
        
        model = Payment
        fields = ['account_number']