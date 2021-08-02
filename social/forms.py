from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from .models import Post

class UserRegisterForm(UserCreationForm):
	username=forms.CharField(label='Usuario')
	email = forms.EmailField()
	password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)
	image = forms.ImageField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2','image']
		#removemos los textos de ayuda que nos da por defecto django
		help_texts = {k:"" for k in fields }

class PostForm(forms.ModelForm):
	content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':2, 'placeholder': '¿Qué está pasando?'}), required=True)

	class Meta:
		model = Post
		fields = ['content']