from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Sale, Purchase, Product, LowStockNotification

@receiver(post_save, sender=Sale)
def decrease_stock_on_sale(sender, instance, created, **kwargs):
    if not created:
        return
    product = instance.product
    product.quantity = product.quantity - instance.quantity
    product.save(update_fields=['quantity', 'updated_at'])
    # create low stock notification if needed
    if product.quantity <= product.alert_number:
        LowStockNotification.objects.create(product=product, quantity=product.quantity)

@receiver(post_save, sender=Purchase)
def increase_stock_on_purchase(sender, instance, created, **kwargs):
    if not created:
        return
    product = instance.product
    product.quantity = product.quantity + instance.quantity
    product.save(update_fields=['quantity', 'updated_at'])
    LowStockNotification.objects.filter(product=product, sent=False).delete()
