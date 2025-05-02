# payments/gateways/payment_gateway.py
from abc import ABC, abstractmethod

class IPaymentGateway(ABC):
    @abstractmethod
    def create_order(self, order_id: int, amount: int, receipt: str) -> dict:
        pass

    @abstractmethod
    def create_payment_link(self, order_id: int) -> dict:
        pass

    @abstractmethod
    def create_payment_link(self, order_id: int, amount: int, name: str, email: str, callback_url=None) -> dict:
        pass

    # @abstractmethod
    # def verify_signature(self, payload: bytes, signature: str) -> bool:
    #     pass