from django.contrib import admin
from stats.models import Upload


class UploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_on', 'file', 'pk')
    list_filter = ('uploaded_on',)
    search_fields = ['title', 'uploaded_on']


admin.site.register(Upload, UploadAdmin)
