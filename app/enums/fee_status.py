from enum import Enum


class FeeStatus(str, Enum):
    PAID = "Paid"
    PENDING = "Pending"
    PARTIAL = "Partial"