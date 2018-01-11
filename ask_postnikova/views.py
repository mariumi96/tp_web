#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.views.generic import View
from ask.models import Question,Answer,Tag,Profile
from ask.forms import QuestionForm,RegistrationForm,AnswerForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView


class QuestionsView(View):
    def get(self,request):
        questions = Question.objects.all()
        questions = paginate(questions, request)
        return render(request, 'index.html', {'questions': questions})


class BestQuestionsView(View):
    def get(self,request):
        choices = Question.objects.best_questions()
        choices = choices[:5]
        questions = paginate(choices, request)
        return render(request, 'index.html', {'questions': questions})


class NewQuestionsView(View):
    def get(self,request):
        choices = Question.objects.new_questions()
        questions = paginate(choices, request)
        return render(request, 'index.html', {'questions': questions})


class QuestionView(View):
    def get(self,request, id):
        q = Question.objects.get(pk=id)
        answers = Answer.objects.filter(question=q)
        answers = paginate(answers, request)
        form = AnswerForm
        return render(request,"questions.html",{"question": q,"answers": answers,"form":form})

    def post(self, request,id):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
        q = Question.objects.get(pk=id)
        answers = Answer.objects.filter(question=q)
        answers = paginate(answers, request)
        form = AnswerForm(data=request.POST,user=profile,id=id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("../question/" + str(id))
        return render(request, 'questions.html', {"question": q,"answers": answers,'form': form})


class QuestionTagView(View):
    def get(self,request, tag_name):
        tag = Tag.objects.get(name=tag_name)
        choices = Question.objects.filter(tags=tag)
        questions = paginate(choices, request)
        return render(request, 'index.html', {'questions': questions, 'tag_name': tag_name})


class AskView(View):
    def get(self,request):
        form = QuestionForm
        return render(request, 'ask.html', {'form': form})

    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)

        form = QuestionForm(data=request.POST,user=profile)
        if form.is_valid():
            form.save()
            form.save_m2m()
            return HttpResponseRedirect("../question/" + str(Question.objects.latest('id').id))
        return render(request, 'ask.html', {'form': form})

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
         return super(AskView,self).dispatch(request, *args, **kwargs)


def singup_view(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form=RegistrationForm
    return render(request,'singup.html',{'form':form})



def settings_view(request):
    return render(request, 'settings.html')


def paginate(objects_list, request):
    # do smth with Paginator, etc...
    paginator = Paginator(objects_list, 3)  # 3 вопроса на страницу
    page = request.GET.get('page')
    try:
       page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)
    return page


def register(request):
    errors = []
    form = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            errors.append("Введите имя пользователя")
        elif len(username) < 5:
            errors.append("Имя пользователя должно содержать не менее 5 символов")

        email = request.POST.get('email')
        if not email:
            errors.append("Введите адрес эл. почты")

        firstname = request.POST.get('firstname')
        if not firstname:
            errors.append("Введите своё имя")
        else:
            form['firstname'] = firstname

        lastname = request.POST.get('lastname')
        if not lastname:
            errors.append("Введите своё фамилию")
        else:
            form['lastname'] = lastname

        password = request.POST.get('password')
        if not password:
            errors.append("Введите пароль")
        elif len(password) < 8:
            errors.append("Пароль должен содержать не менее 8 символов")
        else:
            confirmpass = request.POST.get('confirmpass')
            if not confirmpass:
                errors.append("Подтвердите пароль")
            elif password != confirmpass:
                errors.append("Пароли не совпадают")
                form['confirmpass'] = confirmpass
            form['password'] = password

        sameusers = []
        try:
            sameusers.append(User.objects.get(username=username))
        except User.DoesNotExist:
            form['username'] = username
        try:
            sameusers.append(User.objects.get(email=email))
        except User.DoesNotExist:
            form['email'] = email

        if sameusers:
            errors.append("Пользователь с таким именем или адресом эл. почты уже существует")

        if errors:
            return render(request, 'singup.html', {'errors': errors, 'form': form})

        User.objects.create_user(username=username, email=email, password=password)
        return HttpResponseRedirect("/login/")

    return render(request, 'singup.html', {'errors': [], 'formdata': form})


class SignUpView(View):
    def get(self,request):
        form = RegistrationForm
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
        return render(request, 'signup.html', {'form': form})
