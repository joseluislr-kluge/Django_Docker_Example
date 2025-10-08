from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('places/', views.place_list_view, name='place-list'),
    path('places/add/', views.place_create_view, name='place-create'),
    path('places/update/<str:name>/', views.place_update_view, name='place-update'),
    path('places/delete/<str:name>/', views.place_delete_view, name='place-delete'),
]