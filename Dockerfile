# Utiliza una imagen oficial de Python como base
FROM python:3.12-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala las dependencias necesarias para compilar algunas bibliotecas de Python
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip
RUN pip install --no-cache-dir --upgrade pip

# Copia el archivo requirements.txt en el directorio de trabajo
COPY requirements.txt .

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación en el directorio de trabajo
COPY . .

# Establece la variable de entorno PYTHONPATH
ENV PYTHONPATH=/app/Lesson1

# Configura variables de entorno adicionales si es necesario
ENV MONGO="mongodb"

# Expone el puerto para la aplicación (no es necesario especificar el puerto aquí)
EXPOSE 8000

# Comando para ejecutar la aplicación utilizando la variable de entorno PORT
CMD ["sh", "-c", "cd Lesson1 && python3 -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]