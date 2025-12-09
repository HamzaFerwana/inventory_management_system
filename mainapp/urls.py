from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/create/", views.category_create, name="categories_create"),
    path("categories/", views.categories_index, name="categories_index"),
    path("categories/<int:pk>/edit/", views.category_edit, name="categories_edit"),
    path(
        "categories/<int:pk>/delete/", views.categories_delete, name="categories_delete"
    ),
    path(
        "subcategories/create/", views.subcategory_create, name="subcategories_create"
    ),
    path("subcategories/", views.subcategories_index, name="subcategories_index"),
    path(
        "subcategories/<int:pk>/edit/",
        views.subcategory_edit,
        name="subcategories_edit",
    ),
    path(
        "subcategories/<int:pk>/delete/",
        views.subcategories_delete,
        name="subcategories_delete",
    ),
    path("products/create/", views.product_create, name="products_create"),
    path("products/", views.products_index, name="products_index"),
    path("products/<int:pk>/edit/", views.product_edit, name="products_edit"),
    path("products/<int:pk>/delete/", views.products_delete, name="products_delete"),
    path("customers/", views.customers_index, name="customers_index"),
    path("customers/create/", views.customer_create, name="customers_create"),
    path("customers/<int:pk>/edit/", views.customer_edit, name="customers_edit"),
    path("customers/<int:pk>/delete/", views.customer_delete, name="customers_delete"),
    path("register/", views.register, name="register"),
    path("register_data/", views.register_data, name="register_data"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
