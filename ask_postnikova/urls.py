#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""new_ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from ask_postnikova.views import QuestionsView,ForumView, ArticlesView, TestQuestionView,ResultView,GalleryView, AboutView,BestQuestionsView,WelcomeView,TestView,NewQuestionsView,QuestionTagView, QuestionView,AskView,SettingsView,SignUpView,like_view
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    #url(r'^$', QuestionsView.as_view(), name = "index"),
    url(r'^$', WelcomeView.as_view(), name = "index"),
    url(r'^test_page/',TestView.as_view(), name = "test"),
    url(r'^test/(?P<id>\d+)',TestQuestionView.as_view(),name="test_url"),
    url(r'^result/',ResultView.as_view(), name = 'result'),
    url(r'^forum/',ForumView.as_view(), name = "forum"),
    url(r'^articles/',ArticlesView.as_view(), name = "articles"),
    url(r'^gallery/',GalleryView.as_view(), name = "gallery"),
    url(r'^about/',AboutView.as_view(), name = "about"),
    url(r'^question/(?P<id>\d+)',QuestionView.as_view(),name="question_url"),
    url(r'^tag/(?P<tag_name>\w+)',QuestionTagView.as_view(),name="tag_url"),
    url(r'^login/', LoginView.as_view(template_name='login.html'),name='login'),
    url(r'^signup/', SignUpView.as_view(), name='signup'),
    url(r'^ask/', AskView.as_view(), name='ask'),
    url(r'^settings/', SettingsView.as_view(), name='settings'),
    url(r'^logged_out/', LogoutView.as_view(template_name='index.html'),name = 'logged_out'),
    url(r'^best/',BestQuestionsView.as_view(),name="best_question_url"),
    url(r'^new/',NewQuestionsView.as_view(),name="new_question_url"),
    url(r'^admin/', admin.site.urls),
    url(r'^like/?',like_view),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()


