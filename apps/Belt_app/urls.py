from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    url(r'^$', views.index),
    url(r'login$', views.logins),
    url(r'log$', views.log),
    url(r'new_user$', views.new_user),
    url(r'create$', views.Registration),
    url(r'out$', views.out),
    url(r'new_item$', views.additem),
    url(r'show$', views.show),
    url(r'new$', views.new_quote),
    url(r'(?P<id>\d+)/remove$', views.notfavorite),
    url(r'(?P<id>\d+)/favorites$',  views.favorites),
    url(r'(?P<id>\d+)/by$',  views.showlist),  
    

]