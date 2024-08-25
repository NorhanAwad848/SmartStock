from django.db import models
from datetime import datetime
# Create your models here.

class Item(models.Model):
    name =models.CharField(max_length=100)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=5,decimal_places=2)
    supplier_name=models.CharField(max_length=100)
    description=models.TextField()
    date=models.DateField(default=datetime.now)
    image = models.ImageField(upload_to='images/%y/%m/%d',blank=True,null=True)

    def __str__(self):
        return f"item {self.name} - quantity {self.quantity}"

    class Meta:
        ordering=['date']

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart {self.id} - Created at {self.created_at}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item.name} - Quantity: {self.quantity} in Cart {self.cart.id}"

class Sale(models.Model):
    item = models.ForeignKey(Item,related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"{self.item.name} price  {self.total_price}"