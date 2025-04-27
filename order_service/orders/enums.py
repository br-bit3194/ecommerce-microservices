from enum import Enum

class OrderStatus(Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'