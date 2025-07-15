from django.db import models
from item.models import Item
from django.contrib.auth.models import User
import uuid

class CheckOutOrder(models.Model):
    order_number = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name = 'order'
        ordering = ['-ordered_at']
    
    def __str__(self):
        return f"order #{self.order_number} by:{self.name}"
    
class CheckOutItem(models.Model):
    order = models.ForeignKey(CheckOutOrder, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.FloatField()
    
    def __str__(self):
        return f"#{self.quantity} x {self.item.name}"