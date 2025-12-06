from django.urls import path
from . import views

urlpatterns = [
    path("categories/create/", views.category_create, name="categories_create"),
    path("categories/", views.categories_index, name="categories_index"),
    path("categories/<int:pk>/edit/", views.category_edit, name="categories_edit"),
    path(
        "categories/<int:pk>/delete/", views.categories_delete, name="categories_delete"
    ),
]
