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
]
