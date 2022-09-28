from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.UploadList.as_view(), name='home'),
    path('<str:pk>/', views.UploadDetails.as_view(), name='item'),
    path('upload', views.upload_file, name='upload'),
]
