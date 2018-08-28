from django.shortcuts import render
from django.shortcuts import redirect
from .forms import UploadImageForm
from django.core.files.storage import FileSystemStorage
from opencv_webapp.cameo import Cameo
# Create your views here.

cam = Cameo()
def first_view(request):
  return render(request, 'opencv_webapp/uimage.html', {})


def uimage(request):
  if request.method == 'POST':
      form = UploadImageForm(request.POST, request.FILES)
  if form.is_valid():
      cam.run()
      print('getting response')
      myfile = request.FILES['image']
      fs = FileSystemStorage()
      filename = fs.save(myfile.name, myfile)
      uploaded_file_url = fs.url(filename)
      return render(request, 'opencv_webapp/uimage.html', {'form': form, 'uploaded_file_url': uploaded_file_url})
  else:
      form = UploadImageForm()
      return render(request, 'opencv_webapp/uimage.html', {'form': form})