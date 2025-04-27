from django.db import models

# Create your models here.
class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Order(AuditModel):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'

    user_id = models.IntegerField()  # Assuming user is represented by an integer ID
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def __str__(self):
        return f"Order #{self.id} with total_price: {self.total_price} & status: {self.status}"

class OrderItems(AuditModel):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    product_id = models.IntegerField()  # Assuming product is represented by an integer ID
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

