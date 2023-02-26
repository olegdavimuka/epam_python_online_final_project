from enum import Enum, unique


@unique
class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    UAH = "UAH"
