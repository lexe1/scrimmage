from datetime import datetime, timezone

import pandas
import pytz
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .forms import UploadForm
from .models import Match, StatLine


def login(request):
    if request.method == 'POST':
        return redirect('home')
    return render(request, 'login.html')


class StatsList(ListView):
    queryset = StatLine.objects.all()
    template_name = 'stats.html'
    paginate_by = 50


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            xls = pandas.ExcelFile(request.FILES['file'])
            for sheet in xls.sheet_names:
                dataframe = pandas.read_excel(
                    xls, sheet_name=sheet, skiprows=2, header=None)
                dataframe = dataframe.reset_index()
                for row in dataframe.itertuples():
                    game_month, dates = sheet.split(' ')
                    date = dates.split('.')
                    game_time = 1
                    game_date = date[0]
                    if len(date) == 2:
                        game_time = date[1]
                    dt = datetime.strptime(
                        f"{game_month} {game_date} 2022 {game_time}", '%b %d %Y %I')
                    # utc_time = dt.replace(tzinfo=timezone.utc)
                    # utc_timestamp = utc_time.timestamp()
                    match_date = {
                        'date': dt,
                    }
                    Match.objects.update_or_create(date=match_date['date'])
                    stat_line = {
                        'match': get_object_or_404(Match, date=dt),
                        'date': dt,
                        'player': row._4,
                        'min': float(row._5.replace(',', '.')),
                        'made_2': row._6,
                        'attempts_2': row._8,
                        'made_3': row._10,
                        'made_3': row._10,
                        'attempts_3': row._12,
                        'made_ft': row._13,
                        'attempts_ft': row._14,
                        'reb_o': row._18,
                        'reb_d': row._19,
                        'assist': row._21,
                        'poa': row._22,
                        'pf': row._23,
                        'fd': row._24,
                        'steals': row._25,
                        'turnovers': row._26,
                        'blocks': row._27,
                    }
                    StatLine.objects.update_or_create(
                        date=stat_line['date'], player=stat_line['player'], defaults=stat_line)
            return redirect('matches')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})


tz = pytz.timezone('Atlantic/Reykjavik')


def match_list(request):
    matches = Match.objects.all()
    # queryset = StatLine.objects.all()
    # matches = []
    # for stat in queryset:
    #     date = stat.date
    #     if date not in matches:
    #         matches.append(date)
    # dt = datetime.fromtimestamp(date, tz).strftime('%m-%d-%y MATCH %I')
    return render(request, 'match_list.html', {'matches': matches})


def match_details(request, pk):
    match = Match.objects.get(id=pk)
    queryset = StatLine.objects.filter(match_id=pk)
    return render(request, 'match_details.html', {'match': match, 'queryset': queryset})
