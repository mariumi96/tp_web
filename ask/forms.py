# -*- coding: utf-8 -*-
from django import forms
from models import Question,User,Profile,Answer,Tag
from django.contrib.auth.forms import UserCreationForm


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(QuestionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        exclude=['snippet','rating','date_created','author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text':forms.Textarea(attrs={'class': 'form-control form-text'}),
            'tags': forms.SelectMultiple(attrs={'class':'form-control'})
        }
        help_texts={
            'title':"Help text for title"
        }

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)
        question.author = self.user

        if commit == True:
            question.save()


        return question

    def clean_text(self):
        text=self.cleaned_data['text']
        if(len(text)<10):
            raise forms.ValidationError(u'Too short!')
        return text


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.id = kwargs.pop('id',None)
        super(AnswerForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Answer
        fields=('text',)
        widgets = {
            'text':forms.Textarea(attrs={'class': 'form-control form-text'}),
        }

    def clean_text(self):
        text=self.cleaned_data['text']
        if(len(text)<10):
            raise forms.ValidationError(u'Too short!')
        return text

    def save(self, commit=True):
        answer = super(AnswerForm, self).save(commit=False)
        answer.author = self.user
        answer.question = Question.objects.get(pk=int(self.id))
        if commit == True:
            answer.save()

        return answer


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



