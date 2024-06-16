from django import forms
from django.core.exceptions import ValidationError
from app.models import Profile, User, Answer
from django.db import models
from django.core.validators import validate_email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
        
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['login', 'email', 'password', 'confirm_password', 'avatar']

    login = forms.CharField(min_length=5, max_length=20, required=True)
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    password = forms.CharField(min_length=6, max_length=32, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=6, max_length=32, required=True, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)
    
    def clean(self):
        super().clean()
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('Passwords don\'t match!')
        
    def init(self, *args, **kwargs):
        super(RegisterForm, self).init(*args, **kwargs)
        self.fields['avatar'].required = False

    # commit = False - вызываем метод, но в базе не сохраняем
    def save(self, commit=True):
        user = User.objects.create_user(username=self.cleaned_data['login'], password=self.cleaned_data['password'], email=self.cleaned_data['email'])
        profile = Profile(user=user)
        if self.cleaned_data['avatar']:
            setattr(profile, 'avatar', self.cleaned_data['avatar'])
        profile.save()
        return user
    
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['login', 'email']

    login = forms.CharField(min_length=5, max_length=20, required=True)
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    
    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['login']
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

    avatar = forms.ImageField(required=False)

    # def save(self, commit=True):
    #     user = User.objects.get(username=self.cleaned_data['login'])
    #     user.username = self.cleaned_data['login']
    #     user.email = self.cleaned_data['email']
    #     user.save()
        
    #     profile = Profile.objects.get(user=user)
    #     profile.avatar = self.cleaned_data['avatar']
    #     profile.save()
    #     return user
    
class QuestionForm(forms.Form):
    title = forms.CharField(min_length=10, max_length=255, required=True)
    text = forms.CharField(min_length=50, max_length=65535, required=True)
    # tagsInput = forms.CharField()

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']