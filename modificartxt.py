# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 16:04:41 2023

@author: Felipe
"""
#----------------------------- COMPLETAR CAMPOS ------------------------------#
##CAMPOS A COMPLETAR

#nombre del archivo .TKA que se desea modificar. (Escribir sin el .TKA)
nombre_archivo = '1geni' 

## Estos son los primeros tres renglones que apareceran en el txt generado.
## Lo dejé así porque es como aparece el txt de referencia (GammaVision)
ren1 = 'TXT MODIFICADO'
ren2 = 'ADQUIRIDO CON GENNIE PARA OPERAR CON WINGELLI'
ren3 = 'MARITO-FELIPE' 

#-----------------------------------------------------------------------------#
#%%
## LIBRERIAS
import pandas as pd
import numpy as np
import math

## IMPORTO ARCHIVO TKA
df = pd.read_csv(nombre_archivo + '.TKA', header=None) #importo como dataframe el archivo TKA
datos_iniciales = df[0:2]
df = df[2:]
initial_zeros = [0, 0, 0]
df = pd.concat([pd.DataFrame(initial_zeros),df])
#%%
## SCRIPT PARA MODIFICAR EL ARCHIVO

#----------------------------- INICIO CAJA NEGRA ------------------------------#

cols = 12 #numero de columnas del nuedo dataframe
rows = math.ceil(df.shape[0]/cols)  #numero de filas del nuevo dataframe

s = np.array(df.iloc[:,0]) #genero un array con los elementos de la columna

#completo los elementos vacíos con NaN's para poder aplicar el reshape luego
arr = np.pad(s.astype(float), (0, rows*cols - s.size), mode='constant', constant_values=np.nan)


dfout = pd.DataFrame(np.reshape(arr,(rows,cols))) #construyo una matriz a partir del array generado anteriormente
dfout.insert(0, 'channel', np.arange(0, df.shape[0], 12)) #inserto columna con el indice de canales
dfout = dfout.fillna('').astype(str).replace('\.0$' , '', regex=True) #reemplazo NaN's por elementos vacíos y remplazo los .0 de los floats
dfout['channel'] = dfout['channel'].astype(str) + ':' #agrego los dos puntos en la primer columna para copiar el formato del txt de referencia


name = nombre_archivo + '_modificado' #nombre del txt a exportar

# dfout.to_csv(name + '.txt',
#           sep = '\t',
#           header=None,
#           index = False)

datos = dfout.to_numpy()
np.savetxt(name + '.txt', datos, fmt='%6s'+'%11s'+'%10s'*11)

lines = ['',ren1, ren2, ren3 + '\n']

#Agrego lineas de texto al archivo txt generado
with open(name + '.txt', 'r+') as f:
    readcontent = f.read()
    f.seek(0, 0)
    f.write('\n'.join(lines))
    f.write(readcontent)

#----------------------------- FIN CAJA NEGRA ------------------------------#