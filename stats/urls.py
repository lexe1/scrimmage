from django.urls import path
from .views import UploadDelete, UploadsList, UploadDetails, UploadDelete, upload_file, StatsList


urlpatterns = [
    path('', StatsList.as_view(), name='stats'),

    # path('upload', UploadCreate.as_view(), name='upload'),

    path('upload', upload_file, name='upload'),
    path('uploads', UploadsList.as_view(), name='uploads'),
    path('<str:pk>/', UploadDetails.as_view(), name='uploaded'),
    path('<str:pk>/delete', UploadDelete.as_view(), name='delete-upload'),
    # path('stats/<str:pk>', StatDetails.as_view(), name='stats-item'),

]
