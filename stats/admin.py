from django.contrib import admin
from stats.models import StatLine, Upload, Match
from django.conf.locale.es import formats as es_formats


es_formats.DATETIME_FORMAT = "m d y h"


class UploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'file')
    list_filter = ('date', )
    search_fields = ['date', ]


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'date')
    list_filter = ('date', )
    search_fields = ['date', ]


class StatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'player', 'min', 'made_2', 'attempts_2', 'made_3', 'attempts_3',
                    'made_ft', 'attempts_ft', 'reb_o', 'reb_d', 'assist', 'poa', 'pf', 'fd',
                    'steals', 'turnovers', 'blocks')
    list_filter = ('date', 'player')
    search_fields = ['date', 'player', 'min']
    ordering = ['id', ]
    es_formats.DATETIME_FORMAT = "m d y h"


admin.site.register(Upload, UploadAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(StatLine, StatsAdmin)
