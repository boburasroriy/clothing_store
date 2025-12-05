from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=255)
    pi = models.CharField("position in inventory", max_length=100, blank=True)  # PI
    alert_number = models.PositiveIntegerField(default=0)  # low stock threshold
    measurements = models.CharField(max_length=255, blank=True)
    pprice_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_sale = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    size = models.CharField(max_length=50, blank=True)
    colour = models.CharField(max_length=50, blank=True)
    comment = models.TextField(blank=True)
    quantity = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} ({self.size} {self.colour})"

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=(('admin','Admin'),('manager','Manager'),('cashier','Cashier')))
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Sale(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='sales')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.product.name} x{self.quantity}"

class Purchase(models.Model):
    supplier_name = models.CharField(max_length=255, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='purchases')
    quantity = models.PositiveIntegerField()
    price_price = models.DecimalField("price paid", max_digits=12, decimal_places=2)
    order_date = models.DateField(default=timezone.now)
    income_date = models.DateField(null=True, blank=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Purchase #{self.id} - {self.product.name} x{self.quantity}"

class LowStockNotification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Low stock: {self.product.name} ({self.quantity})"
