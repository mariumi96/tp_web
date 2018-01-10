# -*- coding: utf-8 -*-
from django import forms
from models import Question,User,Profile
from django.contrib.auth.forms import UserCreationForm
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude=['snippet','rating','date_created']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text':forms.Textarea(attrs={'class': 'form-control form-text'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class':'form-control'})
        }
        help_texts={
            'title':"Help text for title"
        }

    def clean_text(self):
        text=self.cleaned_data['text']
        if(len(text)<10):
            raise forms.ValidationError(u'Too short!')
        return text


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email","first_name",'last_name',"password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



