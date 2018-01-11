# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Fields: username, firstname, lastname,email, password, groups, user_permissions,...
import os
from ask_postnikova import settings

GOOD_RATING = 2


class Profile(models.Model):

    # Откуда будут загружены аватары
    avatar = models.ImageField(upload_to="uploads/avatars/",default="uploads/avatars/avatar.png")

    # Связь 1-к-1
    user = models.OneToOneField(User)


    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            # Если аватар не загружен
            return os.path.join(settings.MEDIA_URL, 'avatars', 'avatar.png')

    def __unicode__(self):
            return u'{0} {1}'.format(self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


# Model manager для Question
class QuestionManager(models.Manager):

    # "Лучшие(популярные) вопросы" - рейтинг выше GOOD_RATING
    def best_questions(self):
        return self.filter(rating__gt=GOOD_RATING).order_by('-rating')
    # Новые вопросы
    def new_questions(self):
        return self.order_by('-date_created')
    #Вопросы по тэгу



class Question(models.Model):

    title = models.CharField(max_length=100)
    snippet = models.TextField(default='')
    text = models.TextField()

    # Связь многие-к-1 : у одного пользователя может быть несколько вопросов
    author = models.ForeignKey(Profile)

    rating = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=timezone.now)

    # Связь многие-ко-многим - у одного вопроса может быть несколько тэгов,
    # и один тэг может ссылаться на несколько вопросов
    tags = models.ManyToManyField('Tag')

    objects = QuestionManager()

    def get_title(self):
        return self.title + '?'

    def get_url(self):
        return '/question{question_id}/'.format(question_id=self.id)

    def get_answers(self):
        return Answer.objects.filter(answer_question_id=self.id)

    def get_answers_count(self):
        q = Question.objects.get(pk=self.id)
        answers = Answer.objects.filter(question=q)
        return answers.count()

    def __unicode__(self):
        return u'{0}'.format(self.title)

    class Meta:
        ordering = ['-title']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):

    text = models.TextField()

    # Связь многие-к-1 : 1 пользователь может писать множество ответов
    author = models.ForeignKey(Profile)


    created_at = models.DateTimeField(default=timezone.now)

    #Many to one reference - one question can have many answers
    question = models.ForeignKey(Question)
    rating = models.IntegerField(default=0)

    def get_url(self):
        return self.question.get_url()

    def __unicode__(self):
        return u'{0} - {1}'.format(self.id, self.text)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Tag(models.Model):

    name = models.CharField(max_length=20)

    def __unicode__(self):
        return u'{0}'.format(self.name)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Like(models.Model):

    author = models.ForeignKey(Profile)
    question = models.ForeignKey(Question, null=False)
    answer = models.ForeignKey(Answer, null=True, blank=True)

    class Meta:
        unique_together = ('author', 'question','answer')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __unicode__(self):
        return u'{0} {1}'.format(self.author.user.first_name,self.author.user.last_name)