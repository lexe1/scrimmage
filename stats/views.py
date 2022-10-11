from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Stat, Upload
from .forms import UploadForm
import pandas
from datetime import datetime
import os


class StatsList(ListView):
    queryset = Stat.objects.all()
    template_name = 'stats.html'
    paginate_by = 50


class UploadsList(ListView):
    queryset = Upload.objects.all()
    template_name = 'uploads.html'
    paginate_by = 15


class UploadDetails(DetailView):
    model = Upload
    template_name = 'uploaded.html'

# def uploaded_details():
#     queryset = Stat.objects.all()
#     return render('upload.html', queryset)


def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # c_time = os.path.getctime(
            #     'uploads/' + str(request.FILES['file']).replace(' ', '_'))
            # file_created = str(datetime.fromtimestamp(c_time)).split('-')
            # year_file_created = file_created[0]

            game_year = datetime.now().year

            xlsm = pandas.ExcelFile(request.FILES['file'])
            for sheet in xlsm.sheet_names:
                dataframe = pandas.read_excel(
                    xlsm, sheet_name=sheet, skiprows=2, header=None)
                dataframe = dataframe.reset_index()
                for row in dataframe.itertuples():
                    game_month, dates = sheet.split(' ')
                    date = dates.split('.')
                    game_time = 1
                    game_date = date[0]
                    if len(date) == 2:
                        game_time = date[1]
                    stat = Stat(
                        date=datetime.strptime(
                            f"{game_month} {game_date} {game_year} {game_time}", '%b %d %Y %I'),
                        player=row._4,
                        min=float(row._5.replace(',', '.')),
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
                    stat.save()
            return redirect('uploads')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})


# class UploadCreate(CreateView):
#     model = Upload
#     template_name = 'upload.html'
#     form_class = UploadForm
#     success_url = reverse_lazy('home')

#     def parse_file():
#         file = Upload.objects.last().file
#         xls = pandas.ExcelFile(file)
#         print(xls)

#         for sheet in xls.sheet_names:
#             dataframe = pandas.read_excel(
#                 xls, sheet_name=sheet, skiprows=2, header=None)
#             dataframe = dataframe.reset_index()
#             for row in dataframe.itertuples():
#                 game_month, dates = sheet.split(' ')
#                 date = dates.split('.')
#                 game_time = 1
#                 game_date = date[0]
#                 if len(date) == 2:
#                     game_time = date[1]
#                 player_game_stats = PlayerGameStats(
#                     date=datetime.strptime(
#                         f"{game_month} {game_date} 2022 {game_time}", '%b %d %Y %I'),
#                     player=row._4,
#                     min=float(row._5.replace(',', '.')),
#                     made_2=row._6,
#                     attempts_2=row._8,
#                     made_3=row._10,
#                     attempts_3=row._12,
#                     made_ft=row._13,
#                     attempts_ft=row._14,
#                     reb_o=row._18,
#                     reb_d=row._19,
#                     assist=row._21,
#                     poa=row._22,
#                     pf=row._23,
#                     fd=row._24,
#                     steals=row._25,
#                     turnovers=row._26,
#                     blocks=row._27,
#                 )
#                 player_game_stats.save()

#         return 0


class UploadDelete(DeleteView):
    model = Upload
    template_name = 'delete.html'
    success_url = reverse_lazy('uploads')
