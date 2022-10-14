from django.contrib import admin
from stats.models import StatLine, Upload
from django.conf.locale.es import formats as es_formats


es_formats.DATETIME_FORMAT = "m d y h"


class UploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_on', 'file', 'id')
    list_filter = ('uploaded_on',)
    search_fields = ['title', 'uploaded_on']


class StatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'player', 'min', 'made_2', 'attempts_2', 'made_3', 'attempts_3',
                    'made_ft', 'attempts_ft', 'reb_o', 'reb_d', 'assist', 'poa', 'pf', 'fd',
                    'steals', 'turnovers', 'blocks')
    list_filter = ('date', 'player')
    search_fields = ['date', 'player', 'min']
    ordering = ['id', ]
    es_formats.DATETIME_FORMAT = "m d y h"


admin.site.register(Upload, UploadAdmin)
admin.site.register(StatLine, StatsAdmin)
