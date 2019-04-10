#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.views.generic import View
from ask.models import Question,Answer,Tag,Profile,Like, TestAnswer,TestQuestion
from ask.forms import QuestionForm,RegistrationForm,AnswerForm,SettingsForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.http import JsonResponse
from django.views.decorators.http import require_POST

class QuestionsView(View):
    def get(self,request):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        questions = Question.objects.all()
        questions,pages = paginate(questions, request)

        return render(request, 'index.html', {'questions': questions,'avatar':avatar_url})

class WelcomeView(View):
    def get(self, request):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        return render(request, 'index.html', {'avatar':avatar_url})

class TestView(View):
    def get(self, request):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        answers = TestAnswer.objects.all()
        for answer in answers:
            if answer.selected:
                answer.selected = False  # clear flags
                answer.save()
        return render(request, 'test.html',{'avatar':avatar_url})


class ResultView(View):
    def get(self, request):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        # get results
        results = []
        answers = TestAnswer.objects.all()
        for answer in answers:
            if answer.selected:
                print(answer.question)
                print(answer.text)
                results.append({
                    'n': answer.question.order,
                    'q': answer.question,
                    'a': answer.text
                })
        # add results analytics with pyknow
        return render(request, 'result.html',{'avatar':avatar_url, 'results': results})


class TestQuestionView(View):
    def get(self, request,id):
        q = TestQuestion.objects.get(order=id)
        if TestQuestion.objects.filter(order=(int(id)+1)):
            n = int(id)+1
        else:
            n = 0
        a = TestAnswer.objects.filter(question=q)
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        return render(request, 'test.html',{'avatar':avatar_url, 'number': id,'next_number':n,'question':q, 'answers':a})

    def post(self, request,id):
        selected = request.POST.get('exampleRadios')
        a_selected = TestAnswer.objects.get(pk=selected)
        a_selected.selected = True
        a_selected.save()
        if TestQuestion.objects.filter(order=(int(id)+1)):
            return HttpResponseRedirect("../test/" + str(int(id) + 1))
        else:
            return HttpResponseRedirect("../result/")



class ForumView(View):
    def get(self, request):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        questions = Question.objects.all()
        questions, pages = paginate(questions, request)
        return render(request, 'forum.html',{'avatar':avatar_url, 'questions':questions})

class ArticlesView(View):
    def get(self, request):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        return render(request, 'articles.html', {'avatar':avatar_url})

class GalleryView(View):
    def get(self, request):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        return render(request, 'gallery.html', {'avatar':avatar_url})

class AboutView(View):
    def get(self, request):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        return render(request, 'author.html', {'avatar':avatar_url})

class BestQuestionsView(View):
    def get(self,request):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        choices = Question.objects.best_questions()
        choices = choices[:5]
        questions = paginate(choices, request)
        return render(request, 'index.html', {'questions': questions,'avatar':avatar_url})


class NewQuestionsView(View):
    def get(self,request):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        choices = Question.objects.new_questions()
        questions = paginate(choices, request)
        return render(request, 'index.html', {'questions': questions,'avatar':avatar_url})


class QuestionView(View):
    def get(self,request, id):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        q = Question.objects.get(pk=id)
        answers = Answer.objects.filter(question=q)
        #answers = paginate(answers, request)
        form = AnswerForm
        return render(request,"questions.html",{"question": q,"answers": answers,"form":form,'avatar':avatar_url})

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
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        return render(request, 'index.html', {'questions': questions, 'tag_name': tag_name,'avatar':avatar_url})


class AskView(View):
    def get(self,request):
        form = QuestionForm
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        return render(request, 'ask.html', {'form': form,'avatar':avatar_url})

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


class SettingsView(View):
    def get(self,request):
        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        form = SettingsForm
        return render(request, 'settings.html', {'form': form,'avatar':avatar_url})

    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)

        avatar_url = ""
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            avatar_url = p.avatar_url()
        form = SettingsForm(request.POST,request.FILES,user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        return render(request, 'settings.html', {'form': form,'avatar':avatar_url})

def paginate(objects_list, request):
    # do smth with Paginator, etc...
    page_range = 3
    paginator = Paginator(objects_list, page_range)  # 3 вопроса на страницу
    page = request.GET.get('page')
    try:
       page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)
    return page,paginator.num_pages

'''
def register(request):
   
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
'''

class SignUpView(View):
    def get(self,request):
        form = RegistrationForm
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
        return render(request, 'signup.html', {'form': form})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@login_required(login_url='/login/')
def like_view(request):
    #print(request.POST['id'])
    q = Question.objects.get(pk=int(request.POST.get('qid')))
    p = Profile.objects.get(user=request.user)
    try:
        like = Like.objects.get(question=q,author=p)
        #print ('like найден')
    except:
        like = Like(question=q,author=p)
        like.save()
        q.rating+=1
        #print ('like не найден, создан')
    likes = q.get_rating()
    return HttpResponse(likes)




