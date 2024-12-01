from django import forms
from .models import Justificativo
#formulario de justificativo
class JustificativoForm(forms.ModelForm):
    class Meta:
        model = Justificativo
        fields = ['motivo']
        widgets = {
            'motivo': forms.Textarea(attrs={'placeholder': 'Motivo de la justificación', 'rows': 3, 'class': 'form-control', 'aria-label': 'Motivo'}),
        }
