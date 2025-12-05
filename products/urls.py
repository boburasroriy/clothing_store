from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('sale/create/', views.create_sale, name='create_sale'),
    path('purchase/create/', views.create_purchase, name='create_purchase'),
    path('sales/', views.sales_list, name='sales_list'),          
    path('purchases/', views.purchases_list, name='purchases_list'),  
    path('dashboard/', views.dashboard, name='dashboard'),
]
