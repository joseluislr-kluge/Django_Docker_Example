from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

app = FastAPI(title="Weather API Demo")

# Almacenamiento en memoria por simplicidad
places = {}

class Place(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

# Función que llama a Open-Meteo (API que nos da los datos del clima)
def get_current_weather(latitude: float, longitude: float):
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m"
        },
        timeout=5
    )
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Error fetching weather data")
    return response.json()

# Regresa la lista de lugares disponibles
@app.get("/places")
def list_places():
    return {"places": list(places.values())}

# Agrega un lugar nuevo
@app.post("/places")
def add_place(place: Place):
    if place.name in places:
        raise HTTPException(status_code=400, detail="Place already exists")

    places[place.name] = place.model_dump()
    return {"message": "Place added", "place": place}

# Accede a los datos (latitud y longitud) de un lugar con su nombre
@app.get("/places/{name}")
def get_place(name: str):
    if name not in places:
        raise HTTPException(status_code=404, detail="Place not found")
    return places[name]

# Actualiza un lugar
@app.put("/places/{name}")
def update_place(name: str, updated: Place):
    if name not in places:
        raise HTTPException(status_code=404, detail="Place not found")

    updated_data = updated.model_dump()
    new_name = updated_data['name']

    if name != new_name:
        if new_name in places:
            raise HTTPException(status_code=400, detail=f"Cannot rename. A place named '{new_name}' already exists.")

        del places[name]
        
        places[new_name] = updated_data
        
        return {"message": f"Place renamed from '{name}' to '{new_name}' and updated.", "place": updated}

    places[name] = updated_data
    return {"message": "Place updated successfully.", "place": updated}

# Elimina un lugar
@app.delete("/places/{name}")
def delete_place(name: str):
    if name not in places:
        raise HTTPException(status_code=404, detail="Place not found")

    del places[name]
    return {"message": "Place deleted"}

# Utiliza Open-Meteo para obtener la información del clima actual de alguno de los lugares guardados
@app.get("/weather/{place_name}")
def get_weather_for_place(place_name: str):
    if place_name not in places:
        raise HTTPException(status_code=404, detail="Place not found")

    place = places[place_name]
    weather = get_current_weather(place["latitude"], place["longitude"])
    weather["current"].pop("interval", None)
    return {
        "place": place,
        "weather": weather["current"]
    }
