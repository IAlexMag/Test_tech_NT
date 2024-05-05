import pandas as pd
import mysql.connector
import os
import time
from dotenv import load_dotenv
from mysql.connector import Error
load_dotenv()

# configuraciones para la conexión a BDD MySQL
mydb = mysql.connector.connect(
    host = os.getenv('HOST'),
    port = os.getenv('PORT'),
    user = os.getenv('USER'),
    password = os.getenv('PASSWORD'),
    database = os.getenv('DATABASE')
)


df = pd.read_csv('files\data_prueba_tecnica.csv')

# Limpieza de datos

#columnas a limpiar
columns = ['id', 'company_id', 'amount', 'created_at', 'status']


#elimina columnas con valores nulos
for column in columns:
    df.dropna(subset=column, inplace = True)

#elimina duplicados en la columna id
df.drop_duplicates(subset=['id'], inplace = True)


#Transformación de datos.

#Convierte las columnas created_at y paid_at a un datetime, usa coerce para convertir datos no analizables a un NaT
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
df['paid_at'] = pd.to_datetime(df['paid_at'], errors='coerce')

#elimina los registros con fecha NaT de la columna created_at
df.dropna(subset=['created_at'], inplace=True)

#formatea a Y-m-d H:M:S ambas columnas
df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
df['paid_at'] = df['paid_at'].dt.strftime('%Y-%m-%d %H:%M:%S')

#rellena valores nulos en columna para su inserción a BD
df.fillna({'paid_at' : '1990-01-01 00:00:00'}, inplace = True)

#ajusta la columna amount a un máximo de dos decimales
df.round({'amount' :2})


#asigna una nueva columna al df convirtiendo amount a string
df['new_string'] = df['amount'].astype(str)
#guarda los indices donde se localiza una e|E
indices = df[df['new_string'].str.contains('e|E')].index
#elimina los índices localizados
df = df.drop(indices)

#ajusta las columnas company_id y id a un máximo de 24 caracteres
df['company_id'] = df['company_id'].str[:24]
df['id'] = df['id'].str[:24]

#asigna valor a nulos en columna name
df.fillna({'name' : 'SIN NOMBRE'}, inplace = True)
#guarda los indices de registros que su comany_id coincide con el company_name especificado
indices = df.query('company_id == "cbf1c8b09cd5b549416d49d2" & name != "MiPasajefy"').index
#sustituye los nombres por el valor especificado
for indice in indices:
    df.loc[indice, 'name'] = 'MiPasajefy'
#guarda los indices donde el company_id es erróneo
indices = df.query('name == "MiPasajefy" & company_id != "cbf1c8b09cd5b549416d49d2"').index
#sustituye los valores de los índices
for indice in indices:
    df.loc[indice, 'company_id'] = 'cbf1c8b09cd5b549416d49d2'

#sustituye los valores en columna status con patrón 0x por un Sin estatus
df['status'] = df['status'].astype(str)

indices = df[df['status'].str.contains('0x')].index

for indice in indices:
    df.loc[indice, 'status'] = 'Sin estatus'

# inserción de datos a tabla SQL
#insertará df_3 a tabla cat_companies validando la existencia de cada company
df_2 = df.groupby(['name', 'company_id'])['id'].count()

df_3 = df_2.reset_index()

try:
    if mydb.is_connected():
        cursor = mydb.cursor()
        for index, row in df_3.iterrows():
            sql = 'CALL validate_companies(%s,%s, @msg)'
            values = (row['company_id'], row['name'])
            cursor.execute(sql, values)
            cursor.execute('SELECT @msg;')
            msg = cursor.fetchone()
            mydb.commit()
            print(msg)
except Error as ex:
    print(f'Error en la inserción de datos: ', ex)
    mydb.rollback()
finally:
    if mydb.is_connected():
        cursor.close()
        print("Cursor cerrado")

#Inserta df a tabla cargos
try:
    if mydb.is_connected():
        cursor = mydb.cursor()
        inicio = time.time()
        count = []

        for index, row in df.iterrows():
            sql = "CALL insert_data(%s,%s,%s,%s,%s,%s,%s,@msg)"
            values = (row['id'], row['name'], row['company_id'], row['amount'], row['status'], row['created_at'], row['paid_at'])
            cursor.execute(sql,values)
            cursor.execute('SELECT @msg')
            msg = cursor.fetchone()
            count.append(msg)
            mydb.commit()
            print(f'{len(count)} : Registros Insertados')
        fin = time.time()
        print(f"{fin - inicio} segundos transcurridos")    
        print(f"{len(count)} columnas insertadas")
        
except Error as e:
    print('Falla en la carga de datos: ',e )
    mydb.rollback()
finally:
    if mydb.is_connected():
        cursor.close()
        mydb.close()
        print("Conexión cerrada")