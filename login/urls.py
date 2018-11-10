from django.views.generic import TemplateView
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('course/', views.post),
    re_path('course/(.+)/$', views.courseLink),#正在創造的功能
]                   #r'^(\.+)/$'