from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from . import services
from .forms import PlaceForm

def dashboard_view(request):
    places = services.get_all_places()
    weather_data = []

    if places is not None:
        for place in places:
            weather = services.get_weather_for_place(place['name'])
            if weather:
                weather_data.append(weather)
    else:
        messages.error(request, "Could not connect to the Weather API service.")

    context = {
        'weather_data': weather_data
    }
    return render(request, 'dashboard/dashboard.html', context)

def place_list_view(request):
    places = services.get_all_places()
    if places is None:
        messages.error(request, "Could not fetch places from the API.")
        places = []
    
    context = {'places': places}
    return render(request, 'dashboard/place_list.html', context)

def place_create_view(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            status_code, response_data = services.create_place(data['name'], data['latitude'], data['longitude'])
            if status_code == 200:
                messages.success(request, f"Place '{data['name']}' added successfully.")
                return redirect('place-list')
            else:
                error_detail = response_data.get('detail', 'An unknown error occurred.')
                messages.error(request, f"Error adding place: {error_detail}")
    else:
        form = PlaceForm()

    return render(request, 'dashboard/place_form.html', {'form': form, 'title': 'Add New Place'})

def place_update_view(request, name):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            status_code, response_data = services.update_place(name, data['name'], data['latitude'], data['longitude'])
            if status_code == 200:
                messages.success(request, f"Place updated to '{data['name']}' successfully.")
                return redirect('place-list')
            else:
                error_detail = response_data.get('detail', 'An unknown error occurred.')
                messages.error(request, f"Error updating place: {error_detail}")
    else:
        place_data = services.get_place_details(name)
        if place_data:
            form = PlaceForm(initial=place_data)
        else:
            messages.error(request, "Place not found.")
            return redirect('place-list')

    return render(request, 'dashboard/place_form.html', {'form': form, 'title': f'Update {name}'})

def place_delete_view(request, name):
    if request.method == 'POST':
        success = services.delete_place(name)
        if success:
            messages.success(request, f"Place '{name}' deleted successfully.")
        else:
            messages.error(request, f"Error deleting place '{name}'.")
        return redirect('place-list')

    place = services.get_place_details(name)
    if not place:
        messages.error(request, "Place not found.")
        return redirect('place-list')
        
    return render(request, 'dashboard/place_confirm_delete.html', {'place': place})