from enum import Enum

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    PAID = "paid"
    CANCELLED = "cancelled"
    FAILED = "failed"
    REFUNDED = "refunded"
    EXPIRED = "expired"