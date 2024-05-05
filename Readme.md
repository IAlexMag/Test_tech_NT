# Prueba Técnica NT Group

## Tabla de contenidos

1. [Información General] (#general-info)
2. [Tecnologías empleadas] (#techs)
3. [seccion 1] (#secc_1)
4. [seccion 2] (#secc_2)


## Información general
***
En este README se colocan los puntos desarrollados para la prueba técnica que contempla 2 puntos:
1. Sección 1 (limpieza, transformación, carga y extracción de datos)
2. Sección 2 creación de una API

En cada punto se detallarán los diferentes retos y métodos empleados para llevar a cabo el desarrolo de la prueba técnica.

* Se integra en la carpeta la base de datos utilizada "test.sql"
* En la conexión a la BDD se empleand variables de entorno las cuales no se incluyen en la carpeta

* Se recomienda trabajar en un entorno virtual

* Se incluye el archivo nb.ipynb como muestra del desarrollo de la sección 1

## Tecnologías

*** 
En el archivo "requirements.txt" se encuentran las librerías empleadas en la prueba técnica, a continuación, se da una breve explicación de las más importantes:

MySQL - Un motor de BDD de código abierto en el cual ya cuento experiencia trabajando, fácil de manejar y emplear en proyectos.

Flask - Microframework de rápida curva de aprendizaje en el que acorde a tus necesidades puedes ir agregando "pluggins" o adicionales que permiten estar complementando poco a poco tu proyecto

## Sección 1 
***
1. Extracción: El archivo en formato .csv es un tipo de archivo que me parece es mas fácil de manejar, ademas que puedes emplear facilmente con la libería pandas, si bien en los argumentos de la función pd.to_csv() se puede ser mas especificos sobre los parámetros para estructurar de mejor manera el archivo, sigue siendo sencillo de manejar.

2. Transformación: Una actividad que en el análisis de datos consume la mayor parte del tiempo, en este caso se siguió la estructura de datos propuesta para su inserción a BDD por lo que se tuvo que realizar diferentes tratamientos como:
* Eliminación y tratamiento de valores nulos: Si bien algunos campos dentro de la estructura propuesta aceptaban valores nulos se tornaba especialmente díficil realizar su inserción a BDD por lo que su tratamiento era la mejor opción para respetar la integridad en la BDD, por otra parte en aquellos campos clave y que se presentaba una información nula de la cual sin ese campo era díficil realizar la identificación ó relación del registro era más viable la opción de eliminar dicho registro.
* Ajuste a formato especificado: acorde a la estructura propuesta se realizaron los ajustes de formato a cada columna, desde convertir a un formato datetime, formatear datos, hasta reemplazar valores (en caso de que fuera posible hacerlo a través de un identificador relacionado con algún otro campo)

* Retos específicos: En el proceso de transformación de datos me encontré con un reto en especifico,fue en manejar los campos a fechas, pues había datos que no se ajustaban desde un principio a dicho formato teniendo que hacer un formateo obligatorio y teniendo que emplear "coerce" para el manejo de las fechas nulas, así como su asignación a un valor predeterminado para su inserción a BDD.

3. Dispersión de la información: A raíz de la estructura propuesta se creo una tabla llamada cat_companies en donde se almacena el id y company_name de cada registro empleando al company_id como PK obligando a realizar una validación en la tabla para la inserción de nuevos registros y así poder continuar con la carga de inforación en la tabla cargo.
### Creación de tablas en MySQL
![image text](/img/Srcipts_create.png)
### Diagrama Entidad- Relación
![image text](/img/e-r.png)

* Transacciones: Para el manejo de las transacciones y la carga de la información a tabla charges se emplearon sp que ayudarán a el control de dichas transacciones realizando las inserciones de información pertinente a charges y aportando a la integridad de nuestra BDD
### sp para validación de compañías
![image text](/img/validate.png)
### sp para carga de información
![image text](/img/insert_cargo.png)

4. SQL: Ya con la tabla charges creada y con una E-R bien definida se creó la vista vw_transacciones_por_día que nos permite identificar el monto y estatus transaccionado por día de cada compañía
### Montos transaccionados
![image text](/img/view.png)

## Seccion 2
1. Clase conjunto con métodos para quitar del set generado el número indicado y validar el número faltante, cada método retorna un valor acorde a cada situación para que la API devuelva una respuesta en formato JSON
### Clase conjunto
![image text](/img/conjunto.png)

2. Métodos permitidos (GET), el usuario podra pasar en la url  extract el número a retirar del conjunto, una vez realizada la acción se le indica al usuario que el número fue eliminado del conjunto
### Ejemplo extracción
![image text](/img/remove.png)
* Si el usuario ingresa un número que previamente ya se removió la api devolverá un mensaje indicando la situación
### Ejemplo de duplicidad
![image text](/img/duplicate.png)
* El usuario podrá visualizar el número faltante en el conjunto en la ruta /view_num
### ejemplo
![imgae text](/img/number_quit.png)
* Si el usario ha eliminado mas de un elemento del conjunto y consulta los números faltantes se le notificará que debe volver a ingresar un número a retirar (el conjunto se volverá a generar)
### Ejemplo más de un número eliminado
![image text](/img/repeat.png)
* Si el usuario ingresa una cadena o un flotante como parámetro se le indicará que debe ingresar un número válido.
### Ejemplo validación
![image text](/img/validate_json.png)
* Si el usuario ingresa un número menor que 0 se indicará que debe ingresar un número en un rango del 1 al 100
![image text](/img/menorque.png)
