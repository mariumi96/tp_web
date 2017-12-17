#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.views.generic import View
from ask.models import Question,Answer,Tag


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
        choices = choices[:5]
        questions = paginate(choices, request)
        return render(request, 'index.html', {'questions': questions})


class QuestionView(View):
    def get(self,request, id):
        q = Question.objects.get(pk=id)
        answers = Answer.objects.filter(question=q)
        answers = paginate(answers, request)
        return render(request,"questions.html",{"question": q,"answers": answers})


class QuestionTagView(View):
    def get(self,request, tag_name):
        tag = Tag.objects.get(name=tag_name)
        choices = Question.objects.filter(tags=tag)
        choices = choices[:5]
        questions = paginate(choices, request)
        return render(request, 'index.html', {'questions': questions})


def ask_view(request):
    return render(request, 'ask.html')


def settings_view(request):
    return render(request, 'settings.html')


def singup_view(request):
    return render(request, 'singup.html')


def login_view(request):
    return render(request, 'login.html')

def logged_out_view(request):
    return render(request, 'logged_out.html')


def tags_disney_view(request):
    return render(request, 'tag_disney.html')


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






'''
from ask.models import AuthorForm
def index(request):
    return render(request,'authors.html',{'articles':models.Article.objects.all().prefetch_related('author')})

def create_author(request):

    if request.method == 'POST':
        form=AuthorForm(request.POST)
        if form.is_valid():
        #birthday = form.cleaned_data['birthday']
        #name = form.cleaned_data['name']
        #models.Author.objects.create(birthday=birthday,name=name)
        form.save()
        ###
        return redirect('/')
    else:
        form = AuthorForm()

    return render(request,'ask.html',{'form': form})
'''