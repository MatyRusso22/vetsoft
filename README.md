# Vetsoft

Aplicación web para veterinarias utilizada en la cursada 2024 de Ingeniería y Calidad de Software. UTN-FRLP

## Integrantes

Russo, Matias Ruben.
Ruival,Pablo Daniel.
Daza,Facundo.
Baroni Rodrigo,Mauro
Sivori, Diego

## Dependencias

- python 3
- Django
- sqlite
- playwright
- ruff

## Instalar dependencias

`pip install -r requirements.txt`

## Iniciar la Base de Datos

`python manage.py migrate`

## Iniciar app

`python manage.py runserver`

## Version actual de la imagen de docker

1.0

## Crear proyecto de docker:

- 1° Pararse en la carpeta vetsoft
- 2° Correr el comando "docker build -t vetsoft-app:1.0 .\." por consola, esto creara la imagen de docker.
- 3° Correr el comando "docker run  --name vetsoft-container -p 8000:8000 vetsoft-app:1.0" para crear e inicializar el container donde se aloja la app.
- 4° Acceder a la app a travez de localhost:8000.

## Correr el proyecto:

- Una vez que creaste el proyecto, y queres volver a correr el containter, solo tenes que ejecutar el comando "docker start vetsoft-container"