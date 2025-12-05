from django.contrib import admin
from .models import Product, Employee, Sale, Purchase, LowStockNotification

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','size','colour','quantity','price_sale','alert_number')
    search_fields = ('name','pi')
    list_filter = ('size','colour')

admin.site.register(Employee)
admin.site.register(Sale)
admin.site.register(Purchase)
admin.site.register(LowStockNotification)
