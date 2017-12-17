from django.conf.urls import url

from ask import views

urlpatterns = [
    url(r'^about/$', views.hello, name='hello'),
]
