from django.urls import path
from . import views

urlpatterns =[
    path('create/', views.create, name='create'),
    path('cart/',views.cart,name='cart'),
    path('generate_report/',views.generate_sales_report,name='generate_report'),
    path('report/',views.report,name='report'),
    path('',views.items,name='items'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/',views.checkout, name='checkout'),
    
]