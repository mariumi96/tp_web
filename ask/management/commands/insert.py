# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ask.models import *
from django.core.management import BaseCommand
import lorem
from django.contrib.auth.models import User
    #The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "Filling the db"

    '''
    # Тэги
    
    t = Tag(name='чтение')
    t.save()
    t = Tag(name='психология')
    t.save()
    t = Tag(name='природа')
    t.save()
    t = Tag(name='спорт')
    t.save()
    t = Tag(name='наука')
    t.save()
    t = Tag(name='мультфильмы')
    t.save()
    t = Tag(name='IT')
    t.save()
    t = Tag(name='будущее')
    t.save()
    t = Tag(name='история')
    t.save()
    t = Tag(name='животные')
    t.save()
    
    # Пользователи БД
    
    u1 = User(username='flower',first_name='Amy',last_name='Johnes',password='123')
    u1.save()
    u2 = User(username='queen', first_name='Mary', last_name='Smith', password='123')
    u2.save()
    u3 = User(username='victory98', first_name='Victoria', last_name='Johnson', password='123')
    u3.save()
    u4 = User(username='gregory', first_name='Gregory', last_name='Smith', password='123')
    u4.save()
    u5 = User(username='artsmile', first_name='Andy', last_name='Chase', password='123')
    u5.save()
    
    # Профили пользователей
    
    p = Profile(avatar = "1.png", user=u1)
    p.save()
    p = Profile(avatar = "2.png", user=u2)
    p.save()
    p = Profile(avatar = "3.png", user=u3)
    p.save()
    p = Profile(avatar = "4.png", user=u4)
    p.save()
    p = Profile(avatar = "5.jpg", user=u5)
    p.save()
    
    # Вопросы
    
    p = Profile.objects.get(pk=2)
    q = Question(title='Вопрос №2', snippet='А вы знаете, что ...', text='Текст',rating=3,author=p)
    q.save()
    
    # Добавление тэга к вопросу
    
    q = Question.objects.get(pk=1)
    tag_reading = Tag.objects.get(name='чтение')
    q.tags.add(tag_reading)
    
    '''

    '''
    # 5 лучших вопросов
    
    choices = Question.objects.best_questions()
    choices = choices[:5]
    for ch in choices:
        print(ch)
        
    '''
    '''
    # Использование lorem
    
    p = Profile.objects.get(pk=2)
    for i in range(30):
        q = Question(title=lorem.sentence(), snippet=lorem.paragraph() , text=lorem.text(), rating=i, author=p)
        q.save()
    '''
    # A command must define handle()
    def handle(self, *args, **options):
        self.stdout.write("Doing All The Things!")