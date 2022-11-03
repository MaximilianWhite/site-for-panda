from django import forms
from django.core.exceptions import ValidationError

import re

from .models import Users_Pands, News, Category

class RegisterForm(forms.Form):
    nickname = forms.CharField(label="Название пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label="Фамилия пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль пользователя", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Подтвердить пароль", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Почта", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ('nickname', 'name', 'surname', 'email', 'password1', 'password2')

    def clean_nickname(self):
        if Users_Pands.objects.filter(nickname_user=self.cleaned_data['nickname']).exists():
            raise ValidationError('Данный никнейм уже существует')
        return self.cleaned_data['nickname']

    def clean_email(self):
        if Users_Pands.objects.filter(email_user=self.cleaned_data['email']).exists():
            raise ValidationError('Данная почта уже занята')
        return self.cleaned_data['email']

class LoginForm(forms.Form):
    nickname = forms.CharField(label="Название пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль пользователя", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ('nickname', 'password')

# ============================================================================= Админ панель
class CreateUserForm(forms.Form):
    nickname = forms.CharField(label="Название пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label="Фамилия пользователя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль пользователя", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Подтвердить пароль", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Почта", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    is_admin = forms.BooleanField(label="Администратор?", widget=forms.CheckboxInput(attrs={'class': 'form-check-label'}))

    class Meta:
        fields = ('nickname', 'name', 'surname', 'email', 'password1', 'password2')

    def clean_nickname(self):
        if Users_Pands.objects.filter(nickname_user=self.cleaned_data['nickname']).exists():
            raise ValidationError('Данный никнейм уже существует')
        return self.cleaned_data['nickname']

    def clean_email(self):
        if Users_Pands.objects.filter(email_user=self.cleaned_data['email']).exists():
            raise ValidationError('Данная почта уже занята')
        return self.cleaned_data['email']

class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match('\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match('\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title

class UpdateUsers(forms.ModelForm):
    class Meta:
        model = Users_Pands
        fields = ('nickname_user', 'password_user', 'name_user', 'surname_user', 'email_user', 'is_admin_user')
        widgets = {
            'nickname_user': forms.TextInput(attrs={'class': 'form-control'}),
            'password_user': forms.TextInput(attrs={'class': 'form-control'}),
            'name_user': forms.TextInput(attrs={'class': 'form-control'}),
            'surname_user': forms.TextInput(attrs={'class': 'form-control'}),
            'email_user': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_admin_user': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
        }

class UpdateNews(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class UpdateCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }