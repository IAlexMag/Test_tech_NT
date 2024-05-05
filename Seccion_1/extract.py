import pandas as pd
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


# configuraciones para la conexión a BDD MySQL
mydb = mysql.connector.connect(
    host = os.getenv('HOST'),
    port = os.getenv('PORT'),
    user = os.getenv('USER'),
    password = os.getenv('PASSWORD'),
    database = os.getenv('DATABASE')
)

# Extrae información desde tabla y la convierte a un dataframe
def extract():
    try:
        if mydb.is_connected():
            query = "SELECT * FROM cargo"
            df = pd.read_sql_query(query, mydb, index_col='id')
            mydb.close()
            return df
    except Error as ex:
        mydb.close()
        print(f'Error en la recuperación de información: {ex}')
    
# recupera el dataframe creado en la variable df 
df = extract()

#reemplaza los valores de la columna updated_at que sean igual el valor espcificado por un valor Nat(nulo o vacío)
df.loc[df['updated_at'] == '1990-01-01 00:00:00', 'updated_at'] = pd.NaT

df.to_csv('files\data_higienizada.csv')
