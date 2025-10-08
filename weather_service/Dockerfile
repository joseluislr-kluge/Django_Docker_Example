# La base de nuestra imagen
FROM python:3.11-slim

WORKDIR /app

COPY . .

# Se instalan dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Se despliega el servidor en localhost:8000 con uvicorn
CMD ["uvicorn", "weather_api:app", "--host", "0.0.0.0", "--port", "8000"]