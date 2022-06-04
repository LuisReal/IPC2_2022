from Pila import Carritos, Nodo

opc = 0

while opc<6:

    print("Menu Principal \n",
    "1. Ingreso de datos\n",
    "2. Nuevo Cliente\n",
    "3. Ver Cliente\n",
    "4. Caja Registradora\n",
    "5. Visualizar Datos\n")

    opc = int(input("Ingrese una opcion a elegir: "))

    if opc == 1:
        pila = Carritos()
        carritos = int(input("Ingrese cantidad de carritos: "))

        for a in range(carritos):
            pila.apilar(Nodo(a+1))

        pila.recorrerPila()
        pila.desapilar()
        pila.recorrerPila()
        pila.desapilar()
        pila.recorrerPila()

    elif opc == 2:
        print("Nuevo cliente")
    
    elif opc == 3:
        print("Ver cliente")
    
    elif opc == 4:
        print("Caja Registradora")
    
    elif opc == 5:
        print("Visualizar Datos")
    
    else:
        print("saliendo.....")