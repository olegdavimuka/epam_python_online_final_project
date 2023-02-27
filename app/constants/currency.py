from enum import Enum, unique


@unique
class Currency(Enum):
    """
    An enumeration of currencies used by the application.
    """

    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    UAH = "UAH"
