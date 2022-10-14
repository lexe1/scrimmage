from django.urls import path
from .views import UploadDelete, UploadsList, UploadDelete, StatsList,  upload_file, uploaded_details


urlpatterns = [
    path('', StatsList.as_view(), name='stats'),
    path('upload', upload_file, name='upload'),
    path('uploads', UploadsList.as_view(), name='uploads'),
    path('<int:pk>/', uploaded_details, name='uploaded'),
    path('<int:pk>/delete', UploadDelete.as_view(), name='delete-upload'),

]
