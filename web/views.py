from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .forms import FileCreationForm
from .models import File
import subprocess

# Create your views here.

granted_access = []
waiting_access = []

def index(request):
    
    ip = request.META['REMOTE_ADDR']
    ip = ip.replace(".","")
    #ip, is_routable = get_client_ip(request)
    ip = ip.replace(".","")
    if(ip in granted_access):
        return render(request, 'index.html', {})
    elif(ip not in waiting_access):
        waiting_access.append(ip)
    import pyqrcode
    qr = pyqrcode.create(ip)
    qr.png("/var/www/sharepi-web-app/static/images/qrcode.png", scale=6)
    return render(request, 'index.html', {"file":"qrcode.png"})

def file_form(request):
    ip = request.META['REMOTE_ADDR']
    ip = ip.replace(".","")
    if(ip in granted_access):
        return render(request, 'form.html', {'form': FileCreationForm})
    else:
        return HttpResponseRedirect("/")
        
def file_post(request):
    if request.method == 'POST':
        the_file = File(name=request.POST['name'], file=request.FILES['file'])
        the_file.save()
    return HttpResponseRedirect('/')

def file_view(request):
    return render(request, 'list.html', {})

def request_access(request):
    code = request.GET["code"]
    if(code in  waiting_access):
        granted_access.append(code)
        waiting_access.remove(code)
        response = {"status" : "success"}
    else:
        response = {"status" : "failed"}
    return JsonResponse(response)
