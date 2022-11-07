from datetime import datetime

import pandas
import pytz
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from django.db.models import Sum

from .forms import UploadForm
from .models import Match, StatLine


def login(request):
    if request.method == 'POST':
        return redirect('home')
    return render(request, 'login.html')


def aggregation(request):
    # from = request.args.forms
    # to = request.args.to
    queryset = StatLine.objects.all()
    players = []
    for stat in queryset:
        x = stat.player
        if x not in players:
            players.append(x)
    players_agg = []
    for x in players:
        agg_line = StatLine.objects.filter(player=x).aggregate(
            sum_min=Sum('min'),
            sum_made_2=Sum('made_2'),
            sum_attempts_2=Sum('attempts_2'),

            sum_made_3=Sum('made_3'),
            sum_attempts_3=Sum('attempts_3'),

            sum_made_ft=Sum('made_ft'),
            sum_attempts_ft=Sum('attempts_ft'),

            sum_reb_o=Sum('reb_o'),
            sum_reb_d=Sum('reb_d'),

            sum_assist=Sum('assist'),
            sum_poa=Sum('poa'),
            sum_pf=Sum('pf'),
            sum_fd=Sum('fd'),
            sum_steals=Sum('steals'),
            sum_turnovers=Sum('turnovers'),
            sum_blocks=Sum('blocks'),
        )

        agg_line['player'] = x
        agg_line['sum_min'] = round(agg_line['sum_min'], 2)

        agg_line['percentage_2'] = 0
        if agg_line['sum_attempts_2'] != 0 and agg_line['sum_made_2'] != 0:
            agg_line['percentage_2'] = agg_line['sum_made_2'] / \
                agg_line['sum_attempts_2']
            agg_line['percentage_2'] = round(agg_line['percentage_2'], 2)

        agg_line['percentage_3'] = 0
        if agg_line['sum_attempts_3'] != 0 and agg_line['sum_made_3'] != 0:
            agg_line['percentage_3'] = agg_line['sum_made_3'] / \
                agg_line['sum_attempts_3']
            agg_line['percentage_3'] = round(agg_line['percentage_3'], 2)

        agg_line['percentage_ft'] = 0
        if agg_line['sum_attempts_ft'] != 0 and agg_line['sum_made_ft'] != 0:
            agg_line['percentage_ft'] = agg_line['sum_made_ft'] / \
                agg_line['sum_attempts_ft']
            agg_line['percentage_ft'] = round(agg_line['percentage_ft'], 2)

        agg_line['sum_reb_t'] = agg_line['sum_reb_o'] + agg_line['sum_reb_d']

        players_agg.append(agg_line)

    return render(request, 'aggregation.html', {
        'players_agg': players_agg,
    }
    )


class StatsList(ListView):
    queryset = StatLine.objects.all()
    template_name = 'home.html'
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
    return render(request, 'match_list.html', {'matches': matches})


def match_details(request, pk):
    match = Match.objects.get(id=pk)
    queryset = StatLine.objects.filter(match_id=pk)
    return render(request, 'match_details.html', {'match': match, 'queryset': queryset})
