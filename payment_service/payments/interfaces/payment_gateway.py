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
    def create_payment_link(self, request_id: str, order_id: int, amount: int, name: str, email: str, callback_url=None) -> dict:
        pass

    # @abstractmethod
    # def payment_link_callback(self, request_id: str, order_id: int, payment_id: str) -> dict:
    #     pass

    @abstractmethod
    def verify_payment_link_signature(self, request_id: str, razorpay_payment_id: str, razorpay_payment_link_id: str, razorpay_signature: str):
        pass