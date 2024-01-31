from django import forms
from .models import MarkSheet

class MarkSheetForm(forms.ModelForm):
    class Meta:
        model = MarkSheet
        exclude = ['total_marks']