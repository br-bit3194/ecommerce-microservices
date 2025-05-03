from django.db import models

# Create your models here.
class AuditLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AuditLog(id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})"

class Payment(AuditLog):
    order_id = models.CharField(max_length=255)
    razorpay_order_id = models.CharField(max_length=255, unique=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, unique=True, null=True)
    razorpay_payment_link_id = models.CharField(max_length=255, unique=True, null=True)
    razorpay_short_url = models.CharField(max_length=255, unique=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=50)
    receipt = models.CharField(max_length=255, unique=True)
    reason = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Payment(order_id={self.order_id}, amount={self.amount}, currency={self.currency}, status={self.status})"

