# Imagen base de Python
FROM python:3.11

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar todo el contenido del bot
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el bot
CMD ["python", "main.py"]
