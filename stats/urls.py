from django.urls import path, include
from .views import StatsList, upload, match_list, match_details, login
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', StatsList.as_view(), name='home'),
    path('upload', upload, name='upload'),
    path('matches', match_list, name='matches'),
    path('matches/<int:pk>', match_details, name='match'),
]
