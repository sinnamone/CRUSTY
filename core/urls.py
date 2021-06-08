from django.urls import path,re_path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('', views.button, name='home'),
    path('external', views.external, name='external'),
    path('upload/', views.Upload, name='Upload'),
    re_path(r'^.*\.*', views.pages, name='pages'),
]
