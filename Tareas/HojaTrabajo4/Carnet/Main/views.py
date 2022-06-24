from django.shortcuts import render

# Create your views here.

def carnet(request):
    return render(request, "identificacion.html", {})