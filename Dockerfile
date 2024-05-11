# Establece la imagen base como Python 3.12 en una versión slim
FROM python:3.12-slim


# Instala paquetes necesarios para compilar dependencias de Python
RUN apt-get update && \
    apt-get install -y build-essential libffi-dev libssl-dev
# Establece el directorio de trabajo dentro del contenedor como /app
WORKDIR /app
COPY . /app/

# Copia el archivo requirements.txt del directorio local al directorio /app en el contenedor
COPY requirements.txt .

# Instala las dependencias del proyecto listadas en requirements.txt utilizando pip,
RUN pip install --no-cache-dir --no-cache --disable-pip-version-check -r requirements.txt

# Expone el puerto 8000 para que pueda ser accesible desde fuera del contenedor
EXPOSE 8000

# Define el comando predeterminado para ejecutar la aplicación cuando el contenedor se inicie,
# dentro tambien agrego un apartado para poder realizar las migraciones de la db
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
