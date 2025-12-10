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
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "categories/export/pdf/",
        views.export_categories_pdf,
        name="export_categories_pdf",
    ),
    path(
        "categories/export/excel/",
        views.export_categories_excel,
        name="export_categories_excel",
    ),
    path("products/export/pdf/", views.export_products_pdf, name="export_products_pdf"),
    path(
        "products/export/excel/",
        views.export_products_excel,
        name="export_products_excel",
    ),
    path(
        "subcategories/export/pdf/",
        views.export_subcategories_pdf,
        name="export_subcategories_pdf",
    ),
    path(
        "subcategories/export/excel/",
        views.export_subcategories_excel,
        name="export_subcategories_excel",
    ),
    path(
        "expense-categories/",
        views.expense_categories_index,
        name="expense_categories_index",
    ),
    path(
        "expense-categories/create/",
        views.expense_category_create,
        name="expense_categories_create",
    ),
    path(
        "expense-categories/<int:pk>/edit/",
        views.expense_category_edit,
        name="expense_categories_edit",
    ),
    path(
        "expense-categories/<int:pk>/delete/",
        views.expense_category_delete,
        name="expense_categories_delete",
    ),
    path("expenses/", views.expenses_index, name="expenses_index"),
    path("expenses/create/", views.expense_create, name="expenses_create"),
    path("expenses/<int:pk>/edit/", views.expense_edit, name="expenses_edit"),
    path("expenses/<int:pk>/delete/", views.expense_delete, name="expenses_delete"),
    path("suppliers/", views.suppliers_index, name="suppliers_index"),
    path("suppliers/create/", views.supplier_create, name="suppliers_create"),
    path("suppliers/<int:pk>/edit/", views.supplier_edit, name="suppliers_edit"),
    path("suppliers/<int:pk>/delete/", views.supplier_delete, name="suppliers_delete"),
    path("quotations/", views.quotations_index, name="quotations_index"),
    path("quotations/create/", views.quotation_create, name="quotations_create"),
    path("quotations/<int:pk>/edit/", views.quotation_edit, name="quotations_edit"),
    path(
        "quotations/<int:pk>/delete/", views.quotation_delete, name="quotations_delete"
    ),
    path("purchases/", views.purchases_index, name="purchases_index"),
    path("purchases/create/", views.purchase_create, name="purchases_create"),
    path("purchases/<int:pk>/edit/", views.purchase_edit, name="purchases_edit"),
    path("purchases/<int:pk>/delete/", views.purchase_delete, name="purchases_delete"),
    path(
        "purchases/adjust-quantity/",
        views.purchase_adjust_quantity,
        name="purchases_adjust_quantity",
    ),
    path(
        "purchases/<int:pk>/more-options/",
        views.purchase_more_options,
        name="purchases_more_options",
    ),
]
