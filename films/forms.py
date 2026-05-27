from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from image_uploader_widget.widgets import ImageUploaderWidget

class ExampleForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': ImageUploaderWidget(),
        }
        fields = '__all__'