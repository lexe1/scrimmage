from django import forms
from django.forms import ModelForm
from .models import Upload


class UploadForm(ModelForm):
    title = forms.CharField()
    # slug = forms.SlugField()
    file = forms.FileField()

    class Meta:
        model = Upload
        fields = ['title', 'file']
