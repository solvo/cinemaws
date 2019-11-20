# cinemaws

Este repositorio es desarrollado para impartir talleres de Django en 
la elaboración de servicio web con Django Rest Framework.

Este repositorio está ideado para trabajarse con los tags de git, por lo que se 
recomienda iniciar haciendo 

git checkout -b v0.1 tags/v0.1

Se abordarán los temas:

## Introducción a Django.

- Instalación y configuración del entorno de desarrollo
- Creación del proyecto y gestión del entorno virtual.
- Creación de modelos y migraciones para una base de datos en sqlite.
- Introducción a la vistas administrativas.
- Manipulación de modelos y QuerySet
- Generación de vistas por función para atender servicios

## Introducción a los servicios web con DRF.

- Creación de serializadores.
- Creación de vistas genéricas a partir de modelos y serializadores.
- Conexión con clientes externos como Portman, DRF Html view, y Python con requests.
- Diferentes mecanismos de autenticación

## Algunas acciones de las vistas y gestión de pagos

- Filtros y paginación en vistas.
- Pagos electrónicos.

# Construcción del proyecto 

Cree un entorno virtual

   virtualenv -p python3 .env
   source .env/bin/activate
   pip install -r requirements.txt
   
En caso de iniciar desde 0 debe hacer lo siguiente

    pip install django
    django-admin startproject mvtheater_prj
    cd mvtheater_prj
    python manage.py startapp mvthater
    

# Creación de migraciones

Para crear la base de datos se debe ejecutar

   python manage.py migrate

Para crear las migraciones en la base de datos se debe ejecutar

   python manage.py makemigrations
   python manage.py migrate
   
# Ejecución de la aplicación

Para ejecutar un servidor web de desarrollo se ejecuta

   python manage.py runserver

Este servidor se reinicia cada vez que hay una modificación en un archivo


# Creación de un usuario superadministrador

Los usuarios super administradores son aquellos que tienen acceso a todos los modelos
de la base de datos, generalmente son creados como mencanismos de respaldo, no se recomienda
usarlos como usuarios de la plataforma si esta crea vistas fuera de la vista administrativa

    python manage.py createsuperuser   
  
# Volcado de datos de la DB a Json y  cargado de datos desde Json a DB 

En muchas ocaciones se necesita migrar los datos de una base de datos a otra de forma
simple, django tiene los siguientes utilitarios para esta tarea.

Para extraer la información y cargarla a disco se usa:

  python manage.py dumpdata appname appname.model > data.json
  
Donde appname corresponde a la aplicación que deseamos transformar, tambíen se puede hacer con modelos poniendo appname.model donde 
model es el nombre del modelo en minusculas.

Para cargar la información desde un archivo de json se ejecuta

  python manage.py loaddata data.json
  
  