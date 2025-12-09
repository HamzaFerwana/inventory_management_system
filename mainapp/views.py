from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Category, SubCategory, Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#added views
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from datetime import datetime

@login_required
def index(request):
    return render(request, "index.html")

@login_required
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

@login_required
def categories_index(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "categorylist.html", {"categories": categories})

@login_required
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

@login_required
def categories_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("categories_index")
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect("categories_index")

@login_required
def subcategories_index(request):
    subcategories = SubCategory.objects.select_related("category").order_by("name")
    return render(
        request,
        "subcategorylist.html",
        {"subcategories": subcategories},
    )

@login_required
def subcategory_create(request):
    errors = []

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        code = request.POST.get("code", "").strip()
        description = request.POST.get("description", "").strip()
        category_id = request.POST.get("category_id")

        if not name:
            errors.append("Subcategory name is required.")
        if not code:
            errors.append("Subcategory code is required.")
        if not category_id:
            errors.append("Category is required.")

        if code and SubCategory.objects.filter(code=code).exists():
            errors.append("Subcategory code must be unique.")

        category = None
        if category_id:
            category = Category.objects.filter(pk=category_id).first()
            if not category:
                errors.append("Selected category does not exist.")

        if not errors:
            SubCategory.objects.create(
                name=name,
                code=code,
                description=description or None,
                category=category,
            )
            messages.success(request, "Subcategory created successfully!")
            return redirect("subcategories_index")

        old = {
            "name": name,
            "code": code,
            "description": description,
            "category_id": category_id,
        }
    else:
        old = {}

    context = {
        "errors": errors,
        "old": old,
        "categories": Category.objects.all().order_by("name"),
    }
    return render(request, "addsubcategory.html", context)

@login_required
def subcategory_edit(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    errors = []

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        code = request.POST.get("code", "").strip()
        description = request.POST.get("description", "").strip()
        category_id = request.POST.get("category_id")

        if not name:
            errors.append("Subcategory name is required.")
        if not code:
            errors.append("Subcategory code is required.")
        if not category_id:
            errors.append("Category is required.")

        if (
            code
            and SubCategory.objects.filter(code=code)
            .exclude(pk=subcategory.pk)
            .exists()
        ):
            errors.append("Subcategory code must be unique.")

        category = None
        if category_id:
            category = Category.objects.filter(pk=category_id).first()
            if not category:
                errors.append("Selected category does not exist.")

        if not errors:
            subcategory.name = name
            subcategory.code = code
            subcategory.description = description or None
            subcategory.category = category
            subcategory.save()
            messages.success(request, "Subcategory updated successfully!")
            return redirect("subcategories_index")

        old = {
            "name": name,
            "code": code,
            "description": description,
            "category_id": category_id,
        }
    else:
        old = {
            "name": subcategory.name,
            "code": subcategory.code,
            "description": subcategory.description or "",
            "category_id": subcategory.category_id,
        }

    context = {
        "errors": errors,
        "old": old,
        "subcategory": subcategory,
        "categories": Category.objects.all().order_by("name"),
    }
    return render(request, "editsubcategory.html", context)

@login_required
def subcategories_delete(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)

    if request.method == "POST":
        subcategory.delete()
        messages.success(request, "Subcategory deleted successfully.")
        return redirect("subcategories_index")

    subcategory.delete()
    messages.success(request, "Subcategory deleted successfully.")
    return redirect("subcategories_index")

@login_required
def products_index(request):
    products = Product.objects.select_related("sub_category").order_by("name")
    return render(request, "productlist.html", {"products": products})

@login_required
def product_create(request):
    errors = []

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        sub_category_id = request.POST.get("sub_category_id")
        unit = request.POST.get("unit", "").strip()
        sku = request.POST.get("sku", "").strip()
        quantity = request.POST.get("quantity", "0").strip()
        description = request.POST.get("description", "").strip()
        status = request.POST.get("status", "active")
        price = request.POST.get("price", "").strip()
        discount_percentage = request.POST.get("discount_percentage", "0").strip()
        main_image = request.FILES.get("main_image")

        if not name:
            errors.append("Product name is required.")
        if not unit:
            errors.append("Unit is required.")
        if not sku:
            errors.append("SKU is required.")
        if sku and Product.objects.filter(sku=sku).exists():
            errors.append("SKU must be unique.")
        if not price:
            errors.append("Price is required.")

        sub_category = None
        if sub_category_id:
            sub_category = SubCategory.objects.filter(pk=sub_category_id).first()
            if not sub_category:
                errors.append("Selected subcategory does not exist.")

        try:
            quantity_val = int(quantity or 0)
            if quantity_val < 0:
                errors.append("Quantity cannot be negative.")
        except ValueError:
            errors.append("Quantity must be a number.")

        if not errors:
            Product.objects.create(
                name=name,
                sub_category=sub_category,
                unit=unit,
                sku=sku,
                quantity=quantity_val,
                description=description or None,
                status=status,
                price=price or 0,
                discount_percentage=discount_percentage or 0,
                main_image=main_image,
            )
            messages.success(request, "Product created successfully!")
            return redirect("products_index")

        old = {
            "name": name,
            "sub_category_id": sub_category_id,
            "unit": unit,
            "sku": sku,
            "quantity": quantity,
            "description": description,
            "status": status,
            "price": price,
            "discount_percentage": discount_percentage,
        }
    else:
        old = {}

    context = {
        "errors": errors,
        "old": old,
        "subcategories": SubCategory.objects.select_related("category").order_by(
            "category__name", "name"
        ),
    }
    return render(request, "addproduct.html", context)

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    errors = []

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        sub_category_id = request.POST.get("sub_category_id")
        unit = request.POST.get("unit", "").strip()
        sku = request.POST.get("sku", "").strip()
        quantity = request.POST.get("quantity", "0").strip()
        description = request.POST.get("description", "").strip()
        status = request.POST.get("status", "active")
        price = request.POST.get("price", "").strip()
        discount_percentage = request.POST.get("discount_percentage", "0").strip()
        main_image = request.FILES.get("main_image")

        if not name:
            errors.append("Product name is required.")
        if not unit:
            errors.append("Unit is required.")
        if not sku:
            errors.append("SKU is required.")
        if sku and Product.objects.filter(sku=sku).exclude(pk=product.pk).exists():
            errors.append("SKU must be unique.")
        if not price:
            errors.append("Price is required.")

        sub_category = None
        if sub_category_id:
            sub_category = SubCategory.objects.filter(pk=sub_category_id).first()
            if not sub_category:
                errors.append("Selected subcategory does not exist.")

        try:
            quantity_val = int(quantity or 0)
            if quantity_val < 0:
                errors.append("Quantity cannot be negative.")
        except ValueError:
            errors.append("Quantity must be a number.")

        if not errors:
            product.name = name
            product.sub_category = sub_category
            product.unit = unit
            product.sku = sku
            product.quantity = quantity_val
            product.description = description or None
            product.status = status
            product.price = price or 0
            product.discount_percentage = discount_percentage or 0
            if main_image:
                product.main_image = main_image
            product.save()
            messages.success(request, "Product updated successfully!")
            return redirect("products_index")

        old = {
            "name": name,
            "sub_category_id": sub_category_id,
            "unit": unit,
            "sku": sku,
            "quantity": quantity,
            "description": description,
            "status": status,
            "price": price,
            "discount_percentage": discount_percentage,
        }
    else:
        old = {
            "name": product.name,
            "sub_category_id": product.sub_category_id,
            "unit": product.unit,
            "sku": product.sku,
            "quantity": product.quantity,
            "description": product.description or "",
            "status": product.status,
            "price": product.price,
            "discount_percentage": product.discount_percentage,
        }

    context = {
        "errors": errors,
        "old": old,
        "product": product,
        "subcategories": SubCategory.objects.select_related("category").order_by(
            "category__name", "name"
        ),
    }
    return render(request, "editproduct.html", context)

@login_required
def products_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("products_index")

    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect("products_index")


def register(request):
    if request.user.is_authenticated:
        return redirect("categories_index")
    return render(request, "register.html")


def register_data(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        errors = []

        if not username or not email or not password:
            errors.append("All fields are required.")

        if User.objects.filter(username=username).exists():
            errors.append("This username is already taken.")

        if User.objects.filter(email=email).exists():
            errors.append("This email is already in use.")

        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")

        if errors:
            context = {
                "errors": errors,
                "username": username,
                "email": email,
            }
            return render(request, "register.html", context)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        login(request, user)
        return redirect("categories_index")

    return redirect("register")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("categories_index")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        user = None
        if email and password:      
            try:
                u = User.objects.get(email=email)
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect("categories_index")
        else:
            return render(
                request, "login.html", {"error": "Invalid email or password."}
            )

    return render(request, "login.html")


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("categories_index")

class DataExporter:
    @staticmethod
    def export_to_pdf(queryset, fields, title, filename_prefix):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename_prefix}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.3*inch))

        headers = [display_name for _, display_name in fields]
        data = [headers]
        
        for obj in queryset:
            row = []
            for field_name, _ in fields:
             
                value = obj
                for attr in field_name.split('.'):
                    value = getattr(value, attr, '')
                    if value is None:
                        value = ''
                row.append(str(value))
            data.append(row)
        num_cols = len(fields)
        available_width = 6.5 * inch
        col_width = available_width / num_cols
        table = Table(data, colWidths=[col_width] * num_cols)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 6),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*inch))
        footer_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total Records: {queryset.count()}"
        elements.append(Paragraph(footer_text, styles['Normal']))
        
        doc.build(elements)
        return response
    
    @staticmethod
    def export_to_excel(queryset, fields, title, filename_prefix):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = title[:31]

        header_font = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
        header_fill = PatternFill(start_color='4CAF50', end_color='4CAF50', fill_type='solid')
        header_alignment = Alignment(horizontal='center', vertical='center')
        cell_alignment = Alignment(horizontal='center', vertical='center')
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
        num_cols = len(fields)
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=num_cols)
        title_cell = ws.cell(row=1, column=1)
        title_cell.value = title
        title_cell.font = Font(name='Calibri', size=16, bold=True)
        title_cell.alignment = Alignment(horizontal='center', vertical='center')
        
        for col_num, (_, display_name) in enumerate(fields, 1):
            cell = ws.cell(row=3, column=col_num)
            cell.value = display_name
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = border

        for row_num, obj in enumerate(queryset, 4):
            for col_num, (field_name, _) in enumerate(fields, 1):
                # Handle nested attributes
                value = obj
                for attr in field_name.split('.'):
                    value = getattr(value, attr, '')
                    if value is None:
                        value = ''
                
                cell = ws.cell(row=row_num, column=col_num)
                cell.value = str(value)
                cell.alignment = cell_alignment
                cell.border = border
        for col_num in range(1, num_cols + 1):
            column_letter = openpyxl.utils.get_column_letter(col_num)
            max_length = 0
            for cell in ws[column_letter]:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        last_row = ws.max_row + 2
        ws.cell(row=last_row, column=1, 
                value=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total Records: {queryset.count()}")
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename_prefix}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
        
        wb.save(response)
        return response

def export_categories_pdf(request):

    
    queryset = Category.objects.all().order_by('-created_at')
    fields = [
        ('id', 'Category ID'),
        ('name', 'Category Name'),
        ('code', 'Category Code'),
    ]
    
    return DataExporter.export_to_pdf(
        queryset=queryset,
        fields=fields,
        title="Categories Report",
        filename_prefix="categories"
    )

def export_categories_excel(request):
    queryset = Category.objects.all().order_by('-created_at')
    fields = [
        ('id', 'Category ID'),
        ('name', 'Category Name'),
        ('code', 'Category Code'),
    ]
    
    return DataExporter.export_to_excel(
        queryset=queryset,
        fields=fields,
        title="Categories",
        filename_prefix="categories"
    )

def export_products_pdf(request):
    
    queryset = Product.objects.select_related('sub_category', 'sub_category__category').all().order_by('-created_at')
    fields = [
        ('id', 'Product ID'),
        ('name', 'Product Name'),
        ('sku', 'SKU'),
        ('sub_category.category.name', 'Category'),
        ('sub_category.name', 'Sub Category'),
        ('unit', 'Unit'),
        ('quantity', 'Quantity'),
        ('price', 'Price'),
        ('discount_percentage', 'Discount %'),
        ('status', 'Status'),
    ]
    
    return DataExporter.export_to_pdf(
        queryset=queryset,
        fields=fields,
        title="Products Report",
        filename_prefix="products"
    )


def export_products_excel(request):
    queryset = Product.objects.select_related('sub_category', 'sub_category__category').all().order_by('-created_at')
    fields = [
        ('id', 'Product ID'),
        ('name', 'Product Name'),
        ('sku', 'SKU'),
        ('sub_category.category.name', 'Category'),
        ('sub_category.name', 'Sub Category'),
        ('unit', 'Unit'),
        ('quantity', 'Quantity'),
        ('price', 'Price'),
        ('discount_percentage', 'Discount %'),
        ('status', 'Status'),
        ('description', 'Description')
    ]
    return DataExporter.export_to_excel(
        queryset=queryset,
        fields=fields,
        title="Products",
        filename_prefix="products"
    )

def export_subcategories_pdf(request):
    queryset = SubCategory.objects.select_related('category').all().order_by('-created_at')
    fields = [
        ('id', 'Sub Category ID'),
        ('name', 'Sub Category Name'),
        ('code', 'Sub Category Code'),
        ('category.name', 'Parent Category'),
        ('description', 'Description'),
    ]
    
    return DataExporter.export_to_pdf(
        queryset=queryset,
        fields=fields,
        title="Sub Categories Report",
        filename_prefix="subcategories"
    )
def export_subcategories_excel(request):
    
    queryset = SubCategory.objects.select_related('category').all().order_by('-created_at')
    fields = [
        ('id', 'Sub Category ID'),
        ('name', 'Sub Category Name'),
        ('code', 'Sub Category Code'),
        ('category.name', 'Parent Category'),
        ('description', 'Description'),
    ]
    
    return DataExporter.export_to_excel(
        queryset=queryset,
        fields=fields,
        title="Sub Categories",
        filename_prefix="subcategories"
    )