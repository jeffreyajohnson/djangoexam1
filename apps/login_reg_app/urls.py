from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/new$', views.process, name='process'),
	url(r'^users/login$', views.login, name='login'),	
	
]
