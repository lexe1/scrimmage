from django.shortcuts import render
from django.views import generic
from .models import Upload
from .forms import UploadForm
from django.contrib import messages
from django.http import HttpResponseRedirect


class UploadList(generic.ListView):
    queryset = Upload.objects.all()
    template_name = 'home.html'
    paginate_by = 20


class UploadDetails(generic.DetailView):
    model = Upload
    template_name = 'item.html'


# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES['file'])
            form.save()
            messages.success(
                request, "Uploaded successfully.")
        else:
            messages.error(
                request, 'Something went wrong.')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})
