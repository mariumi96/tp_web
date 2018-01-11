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
from django.conf.urls import url
from django.contrib import admin
from views import register,QuestionsView,BestQuestionsView,NewQuestionsView,QuestionTagView, QuestionView,AskView,settings_view,SignUpView
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', QuestionsView.as_view(), name = "index"),
    url(r'^question/(?P<id>\d+)',QuestionView.as_view(),name="question_url"),
    url(r'^tag/(?P<tag_name>\w+)',QuestionTagView.as_view(),name="tag_url"),
    url(r'^login/', login, {'template_name': 'login.html'},name='login'),
    url(r'^signup/', SignUpView.as_view(), name='signup'),
    url(r'^ask/', AskView.as_view(), name='ask'),
    url(r'^settings/', settings_view, name='settings'),
    url(r'^logged_out/', logout,{'next_page':'/'}, name = 'logged_out'),
    url(r'^best/',BestQuestionsView.as_view(),name="best_question_url"),
    url(r'^new/',NewQuestionsView.as_view(),name="new_question_url"),
    url(r'^admin/', admin.site.urls),
]