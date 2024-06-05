from django.urls import reverse

links = [
    {"label": "Home", "href": reverse("home"), "icon": "bi bi-house-door"},
    {"label": "Clientes", "href": reverse("clients_repo"), "icon": "bi bi-people"},
    {"label": "Mascotas", "href": reverse("pets_repo"), "icon": "bi bi-paw"},
    {"label": "Medicamentos", "href": reverse("medicines_repo"), "icon": "bi bi-paw"},
    {"label": "Proveedores", "href": reverse("provider_repo"), "icon": "bi bi-person-fill"}, 
    {"label": "Productos", "href": reverse("products_repo"), "icon": "bi bi-shop"},
    {"label": "Veterinarios", "href": reverse("vet_repo"), "icon": "bi bi-house-heart"},
]


def navbar(request):
    def add_active(link):
        copy = link.copy()

        if copy["href"] == "/":
            copy["active"] = request.path == "/"
        else:
            copy["active"] = request.path.startswith(copy.get("href", ""))

        return copy

    return {"links": map(add_active, links)}
