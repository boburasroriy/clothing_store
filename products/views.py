from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F

from .models import Product, Sale, Purchase
from .decorators import role_required


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required
@role_required(['cashier', 'manager', 'admin'])
def create_sale(request):
    products = Product.objects.all()

    if request.method == 'POST':
        pid = int(request.POST['product_id'])
        qty = int(request.POST['quantity'])
        product = get_object_or_404(Product, pk=pid)

        if product.quantity < qty:
            messages.error(request, f"Not enough stock for {product.name}.")
            return redirect('products:create_sale')

        total_price = qty * product.price_sale
        employee = getattr(request.user, 'employee', None)

        Sale.objects.create(
            employee=employee,
            product=product,
            quantity=qty,
            total_price=total_price
        )

        product.quantity -= qty
        product.save()

        messages.success(request, f"Sale of {product.name} added successfully!")
        return redirect('products:sales_list')

    return render(request, 'create_sale.html', {'products': products})


@login_required
@role_required(['cashier', 'manager', 'admin'])
def create_purchase(request):
    products = Product.objects.all()

    if request.method == 'POST':
        pid = int(request.POST['product_id'])
        qty = int(request.POST['quantity'])
        price_price = float(request.POST['price_price'])
        supplier_name = request.POST.get('supplier_name', '')

        product = get_object_or_404(Product, pk=pid)

        Purchase.objects.create(
            product=product,
            quantity=qty,
            price_price=price_price,
            supplier_name=supplier_name
        )

        product.quantity += qty
        product.save()

        messages.success(request, f"Purchase of {product.name} added successfully!")
        return redirect('products:purchases_list')

    return render(request, 'create_purchase.html', {'products': products})


@login_required
@role_required(['manager', 'admin'])
def dashboard(request):
    total_sales = Sale.objects.aggregate(total=Sum('total_price'))['total'] or 0
    total_purchase_expense = Purchase.objects.aggregate(
        total=Sum(F('price_price') * F('quantity'))
    )['total'] or 0

    overall_profit = total_sales - total_purchase_expense

    top_products = Product.objects.annotate(
        total_sold=Sum('sales__quantity')
    ).order_by('-total_sold')[:10]

    sales_count = Sale.objects.count()
    purchase_count = Purchase.objects.count()

    context = {
        'total_sales': total_sales,
        'total_purchase_expense': total_purchase_expense,
        'overall_profit': overall_profit,
        'top_products': top_products,
        'sales_count': sales_count,
        'purchase_count': purchase_count,
    }

    return render(request, 'dashboard.html', context)


@login_required
@role_required(['cashier', 'manager', 'admin'])
def sales_list(request):
    sales = Sale.objects.select_related('product', 'employee').all().order_by('-date')
    return render(request, 'sales_list.html', {'sales': sales})


@login_required
@role_required(['cashier', 'manager', 'admin'])
def purchases_list(request):
    purchases = Purchase.objects.select_related('product').all().order_by('-order_date')
    return render(request, 'purchases_list.html', {'purchases': purchases})
