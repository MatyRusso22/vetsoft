from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),
    path("pets/", view=views.pets_repository, name="pets_repo"),
    path("pets/nuevo/", view=views.pets_form, name="pets_form"),
    path("pets/editar/<int:id>/", view=views.pets_form, name="pets_edit"),
    path("pets/eliminar/", view=views.pets_delete, name="pets_delete"),
    path("medicines/", view=views.medicines_repository, name="medicines_repo"),
    path("medicines/nuevo/", view=views.medicines_form, name="medicines_form"),
    path("medicines/editar/<int:id>/", view=views.medicines_form, name="medicines_edit"),
    path("medicines/eliminar/", view=views.medicines_delete, name="medicines_delete"),
    path("proveedores/", view=views.provider_repository, name="provider_repo"), 
    path("proveedores/nuevo/", view=views.provider_form, name="provider_form"), 
    path("proveedores/editar/<int:id>/", view=views.provider_form, name="provider_edit"),
    path("proveedores/eliminar/", view=views.provider_delete, name="provider_delete"),
    path("vet/", view=views.vet_repository, name="vet_repo"),
    path("vet/nuevo/", view=views.vet_form, name="vet_form"),
    path("vet/editar/<int:id>/", view=views.vet_form, name="vet_edit"),
    path("vet/eliminar/", view=views.vet_delete, name="vet_delete"), 
]
