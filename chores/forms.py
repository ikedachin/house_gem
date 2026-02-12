from django import forms
from .models import Chore

class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ['title', 'description', 'base_points', 'difficulty']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'base_points': forms.NumberInput(attrs={'step': 1}),
        }
