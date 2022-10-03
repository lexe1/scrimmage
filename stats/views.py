from lib2to3.pgen2.pgen import DFAState
from django.shortcuts import render
from django.views import generic
from .models import PlayerGameStats, Upload
from .forms import UploadForm
from django.contrib import messages
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os


class UploadList(generic.ListView):
    queryset = Upload.objects.all()
    template_name = 'home.html'
    paginate_by = 20


class UploadDetails(generic.DetailView):
    model = Upload
    template_name = 'item.html'


engine = create_engine('sqlite:///db.sqlite3')


def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            c_time = os.path.getctime(
                'uploads/' + str(request.FILES['file']).replace(' ', '_'))
            file_created = str(datetime.fromtimestamp(
                c_time)).split('-')
            year_file_created = file_created[0]

            xlsm = pd.ExcelFile(request.FILES['file'])

            for sheet in xlsm.sheet_names:
                dataframe = pd.read_excel(xlsm, sheet_name=sheet)
                dataframe = dataframe.reset_index()

                for row in dataframe.itertuples():
                    # print(row.index)
                    # print(row)

                    game_month, dates = sheet.split(' ')
                    date = dates.split('.')

                    game_time = 1
                    game_date = date[0]

                    if len(date) == 2:
                        game_time = date[1]

                    # print(game_month)
                    # print(dates)
                    # print(date)
                    # print(datetime.strptime(
                    #     f"{game_month} {game_date} {file_created_year} {game_time}", '%b %d %Y %I'), '\n')

                    if row.index >= 1:
                        player_game_stats = PlayerGameStats(
                            date=datetime.strptime(
                                f"{game_month} {game_date} {year_file_created} {game_time}", '%b %d %Y %I'),
                            player=row._4,
                            min=row._5,
                            made_2=row._6,
                            attempts_2=row._8,
                            made_3=row._10,
                            attempts_3=row._12,
                            made_ft=row._13,
                            attempts_ft=row._14,
                            reb_o=row._18,
                            reb_d=row._19,
                            assist=row._21,
                            poa=row._22,
                            pf=row._23,
                            fd=row._24,
                            steals=row._25,
                            turnovers=row._26,
                            blocks=row._27,
                        )

            # row_to_write = pd.DataFrame(
            #     {'Date': player_game_stats.date},
            #     {'Player': player_game_stats.player},
            #     {'MIN': player_game_stats.min},

            # )

            # row_to_write.to_sql(PlayerGameStats._meta.db_table, if_exists='replace',
            #                     con=engine, index=False)

            messages.success(
                request, "Uploaded successfully.")
        else:
            messages.error(
                request, 'Something went wrong.')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})
