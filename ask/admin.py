# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models

admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Tag)
admin.site.register(models.Profile)
admin.site.register(models.Like)
admin.site.register(models.CatBreed)
admin.site.register(models.DogBreed)
admin.site.register(models.Rodentia)
admin.site.register(models.RodentType)
#admin.site.register(models.Animal)
#admin.site.register(models.Carnivora)
admin.site.register(models.Cat)
admin.site.register(models.Dog)
#admin.site.register(models.CommonInfo)
#admin.site.register(models.StudentInfo)
admin.site.register(models.TestQuestion)
admin.site.register(models.TestAnswer)

