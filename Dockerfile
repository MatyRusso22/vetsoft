# Establece la imagen base como Python 3.12 en una versión slim
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor como /app
WORKDIR /app

# Copia el archivo requirements.txt del directorio local al directorio /app en el contenedor
COPY requirements.txt .

# Instala las dependencias del proyecto listadas en requirements.txt utilizando pip,
# evitando almacenar en caché para reducir el tamaño de la imagen final (-no-cache-dir)
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos los archivos del directorio local al directorio /app en el contenedor
COPY . .

# Expone el puerto 8000 para que pueda ser accesible desde fuera del contenedor
EXPOSE 8000

# Define el comando predeterminado para ejecutar la aplicación cuando el contenedor se inicie,
# en este caso, ejecuta el servidor de desarrollo de Django en el puerto 8000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
