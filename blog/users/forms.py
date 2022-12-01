from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="网名")

    class Meta:
        model = User
        fields = ("username", "first_name")


class UserForm(forms.ModelForm):
    """ User模型的表单，修改first_name """
    first_name = forms.CharField(label="网名")

    class Meta:
        model = User
        fields = ('first_name',)
