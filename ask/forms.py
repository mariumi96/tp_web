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


class RegistrationForm(forms.ModelForm):
    avatar = forms.ImageField()
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username", "email","first_name",'last_name',"password","confirm_password","avatar")

        widgets = {
        'password': forms.PasswordInput(),
        }
        help_texts = {
            'username': "Ваш никнейм (латиница). Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.",
            'password': "Пароль должен состоять из 8 или более символов и не должен содержать только цифры"

        }

    def clean_username(self):
        username=self.cleaned_data['username']
        if not username:
            raise forms.ValidationError("Введите имя пользователя")
        elif len(username) < 5:
            raise forms.ValidationError("Имя пользователя должно содержать не менее 5 символов")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("Введите адрес эл. почты")
        return email

    def clean_first_name(self):
        firstname = self.cleaned_data['first_name']
        if not firstname:
            raise forms.ValidationError("Введите своё имя")
        return firstname

    def clean_last_name(self):
        lastname = self.cleaned_data['last_name']
        if not lastname:
            raise forms.ValidationError("Введите свою фамилию")
        return lastname

    def clean_confirm_password(self):
        passwd = self.cleaned_data['password']
        passwd_to_check = self.cleaned_data['confirm_password']
        if not passwd_to_check:
            raise forms.ValidationError("Подтвердите пароль")
        elif passwd != passwd_to_check:
            raise forms.ValidationError("Пароли не совпадают")
        return passwd_to_check

    def clean_password(self):
        passwd = self.cleaned_data['password']
        if not passwd:
            raise forms.ValidationError("Введите пароль")
        elif len(passwd) < 8:
            raise forms.ValidationError("Пароль должен содержать не менее 8 символов")
        return passwd

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user = User.objects.create_user(self.cleaned_data['username'],self.cleaned_data['email'], self.cleaned_data['password'])
        if commit:
            user.save()
            profile = Profile(user=user,avatar=self.cleaned_data['avatar'])
            profile.save()
        return user



