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
    

