from django.urls import path
from .views import StatsList, aggregation, upload, match_list, match_details, aggregation


urlpatterns = [
    path('', StatsList.as_view(), name='home'),
    path('aggregation', aggregation, name='aggregation'),
    path('upload', upload, name='upload'),
    path('matches', match_list, name='matches'),
    path('matches/<int:pk>', match_details, name='match'),
]
