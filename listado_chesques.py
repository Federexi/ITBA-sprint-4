
import csv 
import sys
import os.path
import datetime

argumentos = sys.argv #guardo en variable los datos pasados por terminal

#Variables pasadas por argumentos:
# archivo = argumentos[1] 
# dni = argumentos[2]
# salida = argumentos[3]
# tipo = argumentos[4]
# estado = argumentos[5]
# rangoFecha = argumentos[6]

if 5 <= len(argumentos) <= 7: #Chequea que la cantidad de arg sea correcta 
    
    archivo = argumentos[1]

    if os.path.exists(archivo): #Chequea si el archivo existe
        
        with open(archivo, 'r') as file:
            fileCSV = csv.reader(file)
            next(fileCSV)
            lista = []
            for row in fileCSV:
                lista.append(row)
            
            dni = argumentos[2]
            listaFiltro1 = []
            for index, l in enumerate(lista): #filtro por dni creando una nueva lista 
                if dni == l[8]:
                    listaFiltro1.append(l)
            if listaFiltro1 == []: #Chequea si el dni existe sino avisa por pantalla y da error
                print('No se encontraron cheques de clientes con el DNI indicado')
                exit(1)
            
            tipo = argumentos[4].upper()
            listaFiltro2 = []
            for index, l in enumerate(listaFiltro1): #filtro por tipo creando una nueva lista 
                if tipo == l[9]:
                    listaFiltro2.append(l)
            if tipo != 'EMITIDO' and tipo != 'DEPOSITADO':
                print('El tipo de cheque indicado es inválido')
                exit(1)
            if listaFiltro2 == []: #Chequea si el tipo existe sino avisa por pantalla y da error
                print('No se encontraron cheques de clientes que coincidan con el DNI y el tipo de cheque indicados')
                exit(1)
            

            if len(argumentos) >= 6: #chequea la existencia del arg[5]
                tieneNum = False
                for c in argumentos[5]: #sabiendo que el arg[5] es opcional y puede ser una fecha o el estado busca si hay un numero para determinar que arg es
                    if c.isdigit():
                        tieneNum = True
                
                if not tieneNum:
                    estado = argumentos[5].upper()
                    listaFiltro3 = []
                    for index, l in enumerate(listaFiltro2): #filtro por estado creando una nueva lista 
                        if estado == l[10]:
                            listaFiltro3.append(l)
                    if estado != 'PENDIENTE' and estado != 'APROBADO' and estado != 'RECHAZADO':
                        print('El estado de cheque indicado es inválido')
                        exit(1)
                    if listaFiltro3 == []: #Chequea si el estado existe sino avisa por pantalla y da error
                        print('No se encontraron cheques de clientes que coincidan con el DNI, el tipo y el estado del cheque indicados')
                        exit(1)

                else:
                    rangoFecha = argumentos[5] #si encuentra un numero en arg[5] determina que es una fecha 
                    listaFiltro3 = []
                    if ':' in rangoFecha:
                        divisor = rangoFecha.split(':') # divido el rango de fechas en 2 strings que parseo a timestamp para comparar
                        desde = divisor[0]
                        hasta = divisor[1]
                        desdeFiltered = desde.replace("/", "-")
                        hastaFiltered = hasta.replace("/", "-")
                        desdeDate = datetime.datetime.strptime(desdeFiltered, "%d-%m-%Y")
                        hastaDate = datetime.datetime.strptime(hastaFiltered, "%d-%m-%Y")
                        desdeTimestamp = int(round(desdeDate.timestamp()))
                        hastaTimestamp = int(round(hastaDate.timestamp()))
                        for index, l in enumerate(listaFiltro2): #filtro por fecha creando una nueva lista
                            if desdeTimestamp <= int(l[6]) <= hastaTimestamp:
                                listaFiltro3.append(l)
                        if listaFiltro3 == []: #Chequea si en el rango de fecha existen, sino avisa por pantalla y da error
                            print('No se encontraron cheques de clientes que coincidan con el DNI y el tipo en el rango de fecha indicado')
                            exit(1)
                    else:
                        print('Indique un rango de fechas en el formato adecuado')
                        exit(1)


            
            if len(argumentos) == 7: #chequea la existencia del arg[6]
                rangoFecha = argumentos[6]
                listaFiltro4 = []
                if ':' in rangoFecha:
                    divisor = rangoFecha.split(':') # divido el rango de fechas en 2 strings que parseo a timestamp para comparar
                    desde = divisor[0]
                    hasta = divisor[1]
                    desdeFiltered = desde.replace("/", "-")
                    hastaFiltered = hasta.replace("/", "-")
                    desdeDate = datetime.datetime.strptime(desdeFiltered, "%d-%m-%Y")
                    hastaDate = datetime.datetime.strptime(hastaFiltered, "%d-%m-%Y")
                    desdeTimestamp = int(round(desdeDate.timestamp()))
                    hastaTimestamp = int(round(hastaDate.timestamp()))
                    for index, l in enumerate(listaFiltro3): #filtro por fecha creando una nueva lista
                        if desdeTimestamp <= int(l[6]) <= hastaTimestamp:
                            listaFiltro4.append(l)
                    if listaFiltro4 == []: #Chequea si en el rango de fecha existen, sino avisa por pantalla y da error
                            print('No se encontraron cheques de clientes que coincidan con el DNI, el tipo y el estado del cheque en el rango de fecha indicado')
                            exit(1)

                else:
                    print('Indique un rango de fechas en el formato adecuado')
                    exit(1)


            
            for index, l in enumerate(listaFiltro1): #filtro por igualdad de numero de cheque segun dni creando una nueva lista
                indice = index + 1
                while indice < len(listaFiltro1):   
                    if l[0] == listaFiltro1[indice][0]:
                        print('Error: Un cheque de este cliente se encuentra duplicado')
                        exit(1)
                    indice = indice +1
                
            if 'listaFiltro4' in globals() or 'listaFiltro4' in locals(): #si la variable existe la uso como valor para una nueva variable
                listaFiltro5 = listaFiltro4
            elif 'listaFiltro3' in globals() or 'listaFiltro3' in locals():
                listaFiltro5 = listaFiltro3
            else:
                listaFiltro5 = listaFiltro2
            

            salida = argumentos[3].upper() #determino el formato de salida 
            if salida == 'PANTALLA': #si es pantalla imprime por terminal
                for num, l in enumerate(listaFiltro5): #recupero los cheques filtrados y los paso como string para una visual mas limpia
                    num = ', '.join(l) 
                    print(num)    
            elif salida == 'CSV': #si es csv creo un timestamp actual
                tiempo = datetime.datetime.now()
                timestampActual = int(round(tiempo.timestamp()))
                FName = dni + '-' + str(timestampActual) + '.csv'
                FContenido = [['FechaOrigen','FechaPago','NumeroCuentaDestino','Valor']] #creo una lista con los nombres de la informacion requerida
                for index, l in enumerate(listaFiltro5): #agrego la informacion requerida de cada cheque que cumplio con los parametros
                    index = []
                    index.append(l[6])
                    index.append(l[7])
                    index.append(l[4])
                    index.append(l[5])
                    FContenido.append(index)
                with open(FName,'w', newline='') as f: #creo el archivo y lo escribo
                    writer = csv.writer(f)
                    writer.writerows(FContenido)
            else:
                print('El formato de salida indicado es inválido') #si el parametro pasado en indice 3 no es valido da error
                exit(1)


    else: #Chequea si el archivo existe sino avisa por pantalla y da error
        print('El archivo no existe o no ha indicado el camino hacia él correctamente')
        exit(1)


else: #si la cant de arg es incorrecta avisa por pantalla y da error
    print('La cantidad de argumentos es incorrecta')
    exit(1)