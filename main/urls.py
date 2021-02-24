from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('main/', TemplateView.as_view(template_name="main.html")),
    path('scrap/', views.scrap, name='scrap'),
]