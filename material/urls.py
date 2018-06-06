from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^login/', views.login),
    url(r'^signup/', views.signup),
    url(r'logout/', views.logout),
    url(r'^editprofile/$', views.editprofile, name='account'),
    url(r'^account/$', views.account, name='account'),
    url(r'^ajax/validate_emai/', views.validate_emai, name='validate-email'),
    url(r'^ajax/validate_user/', views.validate_user),
    url(r'^activate/(?P<token>[^/\n\r]+)', views.activate, name='activate'),
]