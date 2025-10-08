# La base de nuestra imagen
FROM python:3.11-slim

WORKDIR /app

COPY . .

# Se instalan las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Se despliega el servidor en localhost:8000 con gunicorn
CMD ["gunicorn", "ui_service.wsgi:application", "--bind", "0.0.0.0:8000"]