# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from multiselectfield import MultiSelectField
from django.db import models

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Fields: username, firstname, lastname,email, password, groups, user_permissions,...
import os
#from ask_postnikova import settings
GOOD_RATING = 2
PET_TYPE = (
    (0, 'cat'),
    (1, 'dog'),
    (2, 'parrot'),
    (3, 'reptile'),
    (4, 'rodent'),
    (5, 'freshwater')
)
VOICE_TYPE = (
    (0, 'silent'),
    (1, 'normal'),
    (2, 'loud')
)
WOOL_TYPE = (
    (0, 'none'),
    (1, 'short'),
    (2, 'medium'),
    (3, 'long')
)
SIZE = (
    (0, 'small'),
    (1, 'medium'),
    (2, 'big')
)
TEMPER_CHOICES = (
    (0, 'calm'),
    (1, 'kind'),
    (2, 'loyal'),
    (3, 'playful')
)
class Profile(models.Model):

    # Куда будут загружены аватары
    avatar = models.ImageField(upload_to="uploads/avatars/",default="uploads/avatars/avatar.png")

    # Связь 1-к-1
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            #print(self.avatar.url)
            return self.avatar.url
        else:
            # Если аватар не загружен
            pass
            return os.path.join('uploads', 'avatars', 'avatar.png')

    def __str__(self):
            return u'{0}'.format(self.user.username)

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
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)


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

    def get_rating(self):
        q = Question.objects.get(pk=self.id)
        likes = Like.objects.filter(question=q)
        return likes.count()

    def __str__(self):
        return u'{0}'.format(self.title)

    class Meta:
        ordering = ['-title']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):

    text = models.TextField()

    # Связь многие-к-1 : 1 пользователь может писать множество ответов
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)


    created_at = models.DateTimeField(default=timezone.now)

    #Many to one reference - one question can have many answers
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def get_url(self):
        return self.question.get_url()

    def __str__(self):
        return u'{0} - {1}'.format(self.id, self.text)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Tag(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Like(models.Model):

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author', 'question','answer')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return u'{0} {1}'.format(self.author.user.first_name,self.author.user.last_name)


class Pets(models.Model):
    type = models.IntegerField(choices=PET_TYPE, default=0)
    breed = models.CharField(max_length=30)
    voice = models.IntegerField(choices=VOICE_TYPE, default=0)
    wool = models.IntegerField(choices=WOOL_TYPE, default=0)
    size = models.IntegerField(choices=SIZE, default=0)
    temper = MultiSelectField(choices=TEMPER_CHOICES, max_choices=3, default=0)
    points = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Ж'
        verbose_name_plural = 'Жи'

    def __str__(self):
        return u'{0} - {1}'.format(self.type, self.breed)


class TestQuestion(models.Model):
    order = models.IntegerField(default='1',unique=True)
    text = models.TextField()
    next_q1 = models.IntegerField(default='1')
    next_q2 = models.IntegerField(default='1')
    class Meta:
        verbose_name = 'Вопрос теста'
        verbose_name_plural = 'Вопросы теста'

    def __str__(self):
        return u'{0}'.format(self.text)


class TestAnswer(models.Model):
    text = models.CharField(max_length=30)
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, default='0')
    selected = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Ответ теста'
        verbose_name_plural = 'Ответы теста'

    def __str__(self):
        return u'{0}'.format(self.text)


class Breed(models.Model):
    name = models.CharField(max_length=30)
    desc = models.TextField()
    voice = models.IntegerField(choices=VOICE_TYPE, default=0)
    wool = models.IntegerField(choices=WOOL_TYPE, default=0)
    size = models.IntegerField(choices=SIZE, default=0)
    temper = MultiSelectField(choices=TEMPER_CHOICES, max_choices=3, default=0)
    points = models.IntegerField(default=0)

    class Meta:
        #abstract = True
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'

    def __str__(self):
        return u'{0} - {1}'.format(self.name, self.points)

class CatBreed(Breed):
    class Meta:
        verbose_name = 'Порода кошки'
        verbose_name_plural = 'Породы кошек'

    def __str__(self):
        return u'{0} - {1}'.format(self.name, self.points)

class DogBreed(Breed):
    class Meta:
        verbose_name = 'Порода собаки'
        verbose_name_plural = 'Породы собак'

    def __str__(self):
        return u'{0} - {1}'.format(self.name, self.points)

class RodentType(Breed):
    class Meta:
        verbose_name = 'Вид грызуна'
        verbose_name_plural = 'Виды грызунов'

    def __str__(self):
        return u'{0} - {1}'.format(self.name, self.points)

class Animal(models.Model):
    class Meta:
        #abstract = True
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'


class Carnivora(Animal):
    class Meta:
        #abstract = True
        verbose_name = 'Хищное'
        verbose_name_plural = 'Хищные'

class Cat(Carnivora):
    breed = models.ForeignKey(CatBreed, default='0', on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Кошка'
        verbose_name_plural = 'Кошки'

    def __str__(self):
        return u'{0}'.format(self.breed)

class Dog(Carnivora):
    breed = models.ForeignKey(DogBreed, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'

    def __str__(self):
        return u'{0}'.format(self.breed)

class Rodentia(Animal):
    breed = models.ForeignKey(RodentType, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Грызун'
        verbose_name_plural = 'Грызуны'











