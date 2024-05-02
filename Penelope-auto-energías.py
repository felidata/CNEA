# -*- coding: utf-8 -*-
"""
Created on Wed May  1 22:51:45 2024

Autor: Felipe
@mail: felipe.perez.emiliano@gmail.com

Este código permite, dado un archivo input de Penelope (.in), simular la emisión
de fotones de diferentes energías y obtener la curva de eficiencia para una 
dada geometría
"""
#%% COMPLETAR ESTOS CAMPOS

#Carpeta donde se encuentran los archivos necesarios para la simulación
carpeta_origen = r"C:\Users\Felipe\Desktop\CNEA\Codigos\automatizacion-penelope\simulacion-detector10" 

#Definir las energías a simular
energias = [5, 10, 25]

#Input
archivo_input = 'HPGe.in'

#Geometria
geometria = 'HPGe10.geo'

#####---------------------------------------------------------------------#####

import time
import subprocess
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#####---------------------------------------------------------------------#####

#Función para obtener la eficiencia a partir del archivo dump.dat
def eficiencia(output):
    # Nombre del archivo
    archivo = output
    
    # Leer el archivo .dat y almacenar los datos en una lista
    data = []
    with open(archivo, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                values = line.split()
                data.append([float(value) for value in values])
    
    # Convertir los datos en un DataFrame
    df = pd.DataFrame(data, columns=['Energy', 'Density', 'Uncertainty'])
    
    # Encontrar el máximo en la columna 'Density' 
    peak = max(df['Density'])
    
    # Obtener los valores correspondientes al máximo en la columna 'Energy'
    idx = df.index[df['Density'] == peak].tolist()[0]
    
    # Encontrar la resolución en energía 
    delta_energy = df['Energy'][idx + 1] - df['Energy'][idx]
    
    # Cálculo de la eficiencia del detector
    eff = peak * delta_energy
    
    return(eff)

#####---------------------------------------------------------------------#####

## MODIFICACION DE INPUTS

# Lista para almacenar los nombres de los archivos .geo
geometrias = [geometria]

data = [energias]

print('\n //----------------- INICIO SIMULACIÓN--------------------// \n')

inicio = time.time()

for g in range(len(geometrias)):
    eficiencias = []
    for j in range(len(energias)):
        start = time.time()
        nuevo_input = f"E{energias[j]}.in"
        # Bandera para indicar si se ha encontrado la línea "SURFACE (   2)"
        encontrado = False
        
        # Lee el contenido actual del archivo .geo y realiza la modificación necesaria
        with open(archivo_input, "r") as f:
            lineas = f.readlines()
            for i, linea in enumerate(lineas):
                if "SENERG" in linea:
                    encontrado = True
                    nueva_linea = linea[:len('SENERG') + 1] + f"{energias[j]}e3\n"
                    lineas[i] = nueva_linea
                if "GEOMFN" in linea:
                    encontrado = True
                    nueva_linea = linea[:len('GEOMFN') + 1] + f"{geometrias[g]}              [Geometry definition file, 20 chars]"
                    lineas[i] = nueva_linea
        
        # Escribe el contenido modificado en el nuevo archivo .geo
        if encontrado:
            with open(nuevo_input, "w") as f:
                f.writelines(lineas)
            # print("Archivo modificado guardado como:", nuevo_input)
        else:
            print("No se encontró la línea 'SENERG' en el archivo.")
        
        ## SIMULACION DE INPUT DESDE PYTHON
        # Nombre del archivo de salida luego de la simulación
        output = ['dump.dat', 'dump1.dat', 'dump2.dat']
        
        for s in output:
            # Verificar si existe el archivo dump.dat y en caso afirmativo borrarlo
            if os.path.exists(s):
                # Borrar el archivo
                os.remove(s)
                
        # Abrir una nueva ventana de CMD y ejecutar el comando
        print(f'Simulando "{nuevo_input}"...') 
        p = subprocess.run(["cmd", "/c", 'penmain.exe', '<', nuevo_input], cwd=carpeta_origen, capture_output=True, text=True, shell=False)
        
        print(p.stdout)
        
        print(f'Simulación de "{nuevo_input}" terminada.') 
        
        stop = time.time()
        duration = stop-start
        print(f'Duración: {round(duration/60)} minutos.')
        print('\n //--------------------------------------------------// \n')
        
        eficiencias.append(eficiencia(output[0]))
    
    data.append(eficiencias)

final = time.time()

print(f'\n Duración total de la simulación: {round((final-inicio)/60)} minutos.')

#####---------------------------------------------------------------------#####

# Nombre de las columnas
nombres_columnas = ['Energía', 'Eficiencia'] 

# Convertir la lista de listas en un DataFrame
df = pd.DataFrame(np.transpose(np.array(data)), columns=nombres_columnas)

# Printeo el Dataframe
print(df)

# Guarda el DataFrame como un archivo Excel
df.to_excel('simulacion.xlsx', index=False) 

# Configurar el estilo de seaborn
sns.set_style("darkgrid")

# Plot
plt.plot(df['Energía'], df['Eficiencia'], '-o')
plt.xlabel('Energías (keV)')
plt.ylabel('Eficiencias')
plt.title('Simulación Detector 10', family='Serif', fontsize=14)
plt.show()