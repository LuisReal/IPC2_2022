from django.shortcuts import render
import json, requests

def home(request):
    
    return render(request, "Home.html", {})

    

def empleados(request):
    saludo =""
    datos=""
    file=""
    data = ""
    text =""
    nombre=""
    datos =""
    
    if request.POST.get('nombre'):
        data = sendEmpleados()
        text = request.POST.get('texto')
        datos = sendNombre(text)['data']

        #print("el nombre encontrado es: ", nombre[0], " el puesto es: ", nombre[1], " el salario: ", nombre[2])

    if request.POST.get('departamento'):
        data = sendEmpleados()
        text = request.POST.get('texto')
        datos = sendDepartamento(text)
       

    if request.POST.get('sueldo'):
        data = sendEmpleados()
        text = request.POST.get('texto')
        
    if (request.POST.get('ver')):
        data = sendEmpleados()
            #saludo = "hola mundo"
        #file = request.FILES['file']

        #for chunk in file.chunks():
            #datos = str(chunk)
    
        #datos = datos.replace('b\'<?xml version="1.0"?>', " ").replace('\'', ' ').replace("\\r\\n", "\r\n")

    dic = {'data': data, 'saludo':saludo, 'result':text, 'datos': datos}

    return render(request, "Empleados.html", dic )

def discos(request):
    
    saludo =""
    datos=""
    data = ""
    text =""
    
    if request.POST.get('titulo'):
        data = sendDiscos()
        text = request.POST.get('texto')
        datos = sendTitulo(text)

        #print("el nombre encontrado es: ", nombre[0], " el puesto es: ", nombre[1], " el salario: ", nombre[2])

    if request.POST.get('year'):
        data = sendDiscos()
        text = request.POST.get('texto')
        datos = sendYear(text)
       

    if request.POST.get('artista'):
        data = sendDiscos()
        text = request.POST.get('texto')
        datos = sendArtista(text)
        
    if (request.POST.get('ver')):
        data = sendDiscos()

    dic = {'data': data, 'saludo':saludo, 'result':text, 'datos': datos}

    return render(request, "Discos.html", dic)

def paises(request):
    return render(request, "Paises.html", {})

def sendNombre(nombre):
    data = {'nombre': nombre}
    resp =requests.post('http://localhost:9000/empleadoNombre', json=data)
    datos = resp.json()
    return datos

def sendDepartamento(depto):
    data = {'departamento': depto}
    resp =requests.post('http://localhost:9000/empleadoDepartamento', json=data)
    datos = resp.json()
    return datos

def sendEmpleados():

    #resp =requests.get('http://localhost:9000/empleados')
    #datos=resp.json()
    #return render(request,'blog/elemento1.html',{'variable':datos})
    
    #data = {'archivo': datos}

    response = requests.get('http://127.0.0.1:9000/ruta1') # se envia a la api de flask

    datos= response.json()

    return datos # retorna el dato recibido de la api de flask

def sendDiscos():

    response = requests.get('http://127.0.0.1:9000/discos') # se envia a la api de flask

    datos= response.json()

    return datos # retorna el dato recibido de la api de flask

def sendTitulo(text):
    data = {'title': text}
    resp =requests.post('http://localhost:9000/discoTitulo', json=data)
    datos = resp.json()
    return datos

def sendYear(text):
    data = {'year': text}
    resp =requests.post('http://localhost:9000/discoYear', json=data)
    datos = resp.json()
    return datos

def sendArtista(text):
    data = {'artist': text}
    resp =requests.post('http://localhost:9000/discoArtista', json=data)
    datos = resp.json()
    return datos
