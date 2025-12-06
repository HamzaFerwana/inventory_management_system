from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category


def category_create(request):
    errors = []
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        code = request.POST.get("code", "").strip()
        if not name:
            errors.append("Category name is required.")
        if not code:
            errors.append("Category code is required.")
        if Category.objects.filter(code=code).exists():
            errors.append("Category code must be unique.")
        if not errors:
            Category.objects.create(
                name=name,
                code=code,
            )
            messages.success(request, "Category created successfully!")
            return redirect("categories_index")
    context = {
        "errors": errors,
        "old": request.POST if request.method == "POST" else {},
    }
    return render(request, "addcategory.html", context)


def categories_index(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "categorylist.html", {"categories": categories})


def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    errors = []
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        code = request.POST.get("code", "").strip()
        if not name:
            errors.append("Category name is required.")
        if not code:
            errors.append("Category code is required.")
        if code and Category.objects.filter(code=code).exclude(pk=category.pk).exists():
            errors.append("Category code must be unique.")
        if not errors:
            category.name = name
            category.code = code
            category.save()
            messages.success(request, "Category updated successfully!")
            return redirect("categories_index")
        old = {"name": name, "code": code}
    else:
        old = {"name": category.name, "code": category.code}
    context = {
        "errors": errors,
        "old": old,
        "category": category,
    }
    return render(request, "editcategory.html", context)


def categories_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("categories_index")
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect("categories_index")
