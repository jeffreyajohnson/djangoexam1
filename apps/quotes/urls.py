from django.conf.urls import url
from . import views

urlpatterns = [
   	url(r'^favorite/(?P<id>\d+)$', views.favorite, name='favorite'),
   	url(r'^remove/(?P<id>\d+)$', views.remove, name='remove'),
    url(r'^create?$', views.create, name='create'),
    url(r'^logout?$', views.logout, name='logout'),
    url(r'^user/(?P<id>\d+)$', views.user, name='user'),
    url(r'^$', views.index, name='index'),    
]