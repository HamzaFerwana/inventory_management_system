from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


class Category(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="subcategories",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="brands/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
    ]
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="products",
    )
    sub_category = models.ForeignKey(
        "SubCategory",
        on_delete=models.PROTECT,
        related_name="products",
        blank=True,
        null=True,
    )
    brand = models.ForeignKey(
        "Brand",
        on_delete=models.PROTECT,
        related_name="products",
        blank=True,
        null=True,
    )
    unit = models.CharField(max_length=16)
    sku = models.CharField(max_length=255, unique=True)
    minimum_quantity = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="open",
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    main_image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
