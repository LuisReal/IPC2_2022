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
        datos = sendNombre(text)

        #print("el nombre encontrado es: ", nombre[0], " el puesto es: ", nombre[1], " el salario: ", nombre[2])

    if request.POST.get('departamento'):
        data = sendEmpleados()
        text = request.POST.get('texto')
        datos = sendDepartamento(text)
       

    if request.POST.get('sueldo'):
        data = sendEmpleados()
        text = request.POST.get('texto')
        datos = sendSueldo(text)

    if request.POST.get('eliminar'):
        data = sendEmpleados()
        text = request.POST.get('elim')
        eliminarEmpleado(text)

    if request.POST.get('modificar'):
        data = sendEmpleados()
        id = request.POST.get('id')
        nombre = request.POST.get('name')
        puesto = request.POST.get('puesto')
        salario = request.POST.get('salario')

        obj_json = {"id": id, "nombre": nombre, "puesto": puesto, "salario": salario}
        
        modificarEmpleado(obj_json)

    if request.POST.get('reporteEmpleados'):
        
        reporteEmpleados()

        return render(request, "ReporteEmpleados.html", {})
        
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

    if request.POST.get('eliminado'):
        data = sendDiscos()
        text = request.POST.get('elim')
        eliminarDisco(text)

    if request.POST.get('modificar'):
        data = sendDiscos()
        titulo = request.POST.get('titulo1')
        artista = request.POST.get('artista1')
        pais = request.POST.get('pais')
        compania = request.POST.get('compania')
        precio = request.POST.get('precio')
        anio = request.POST.get('anio1')

        obj_json = {"title": titulo, "artist":artista, "country":pais, "company":compania, "price":precio, "year":anio }

        modificarDisco(obj_json)
        
    if (request.POST.get('ver')):
        data = sendDiscos()

    if request.POST.get('reporte'):
        
        reporteDiscos()

        return render(request, "ReporteDiscos.html", {}) #carga la pagina ReporteDiscos.html

    dic = {'data': data, 'saludo':saludo, 'result':text, 'datos': datos}

    return render(request, "Discos.html", dic)

def paises(request):
    data= ""
    datos = ""

    if request.POST.get('ver'):
        data = sendPaises()

    if request.POST.get('moneda'):
        data = sendPaises()
        moneda = request.POST.get('paises')
        datos = sendMoneda(moneda)
    
    if request.POST.get('idioma'):
        data = sendPaises()
        idioma = request.POST.get('paises')
        print("el tipo de variables es: ",type(idioma ))
        datos = sendIdioma(idioma)

    if request.POST.get('continente'):
        data = sendPaises()
        continente = request.POST.get('paises')
        datos = sendContinente(continente)

    if request.POST.get('reporte'):
        
        reportePaises()

        return render(request, "ReportePaises.html", {})

    dic = {'data': data, 'datos':datos}

    return render(request, "Paises.html", dic)

def sendPaises():
    
    response = requests.get('http://127.0.0.1:9000/paises') # se envia a la api de flask

    datos= response.json()

    return datos # retorna el dato recibido de la api de flask

def sendMoneda(moneda):
    data = {'moneda': moneda}
    resp =requests.post('http://localhost:9000/paisMoneda', json=data)
    datos = resp.json()
    return datos

def sendIdioma(idioma):
    data = {'idioma': idioma}
    resp =requests.post('http://localhost:9000/paisIdioma', json=data)
    datos = resp.json()
    return datos

def sendContinente(continente):
    data = {'continente': continente}
    resp =requests.post('http://localhost:9000/continente', json=data)
    datos = resp.json()
    return datos

def reportePaises():

    response = requests.get('http://127.0.0.1:9000/reportePaises') # se envia a la api de flask

    response.json()

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

def sendSueldo(salario):
    data = {'salario': salario}
    resp =requests.post('http://localhost:9000/empleadoSueldo', json=data)
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

def eliminarEmpleado(text):
    data = {'id': text}
    resp =requests.post('http://localhost:9000/eliminarEmpleado', json=data)
    datos = resp.json()

def modificarEmpleado(obj_json):
    
    resp =requests.post('http://localhost:9000/modificarEmpleado', json=obj_json)
    datos = resp.json()

def reporteEmpleados():

    response = requests.get('http://127.0.0.1:9000/reporteEmpleados') # se envia a la api de flask

    datos= response.json()

    

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

def eliminarDisco(text):
    data = {'title': text}
    resp =requests.post('http://localhost:9000/eliminarDisco', json=data)
    datos = resp.json()

def modificarDisco(obj_json):
   
    resp =requests.post('http://localhost:9000/modificarDisco', json=obj_json)
    datos = resp.json()
    
def reporteDiscos():

    response = requests.get('http://127.0.0.1:9000/reporteDiscos') # se envia a la api de flask

    response.json()

    
