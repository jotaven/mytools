from django import forms
from django.utils import timezone
from datetime import timedelta 

class ContextForm(forms.Form):
    text = forms.CharField(label="", max_length=15240, required=True, widget=forms.Textarea(attrs={'class': 'block p-2.5 w-[80vw] md:w-[50vw] text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 resize-y', 'rows':'25', 'placeholder': 'Escreva algo...'}))
    expires_at = forms.ChoiceField(label='Expira em', choices=[(0.083, '5 minuto'), (0.5, '30 minutos'), (1, '1 horas'), (3, '3 horas'), (6, '6 horas'), (12, '12 horas'), (24, '24 horas')], required=True)

    def clean(self):
        cleaned_data = super().clean()
        expires_in_hours = float(cleaned_data.get('expires_at'))
        expires_at_datetime = timezone.now() + timedelta(hours=expires_in_hours)
        cleaned_data['expires_at'] = expires_at_datetime
        return cleaned_data
