# Usar una imagen base de Python oficial y ligera
FROM python:3.9-slim

# Instalar dependencias del sistema, incluyendo ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Crear la carpeta de descargas y dar permisos (por si acaso)
RUN mkdir -p downloads && chmod 777 downloads

# Exponer el puerto que usa Flask (por defecto 5000, pero Render usa la variable PORT)
EXPOSE 5000

# Comando para ejecutar la aplicación usando Gunicorn (servidor de producción)
# Asegúrate de que gunicorn esté en requirements.txt
CMD gunicorn --bind 0.0.0.0:$PORT app:app
