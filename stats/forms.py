from django import forms
from .models import Match, Upload


class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('file', )
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
