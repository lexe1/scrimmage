from asyncio.windows_events import NULL
from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models


class Upload(models.Model):
    title = models.CharField(max_length=50, unique=True)
    file = models.FileField(upload_to='uploads')
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_on']
