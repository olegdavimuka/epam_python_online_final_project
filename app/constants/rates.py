from enum import Enum, unique

from app.constants.currency import Currency


@unique
class Rates(Enum):
    """
    A class that contains enumerated currency exchange rates.

    Attributes:
        USD (dict): the currency rates for United States dollars
        EUR (dict): the currency rates for euros
        GBP (dict): the currency rates for British pounds
        UAH (dict): the currency rates for Ukrainian hryvnias

    Methods:
        get_rate(currency_from: Currency, currency_to: Currency) -> float:
            Returns the exchange rate between two currencies.
    """

    USD = {
        Currency.USD: 1,
        Currency.EUR: 0.95,
        Currency.GBP: 0.84,
        Currency.UAH: 36.76,
    }
    EUR = {
        Currency.USD: 1.05,
        Currency.EUR: 1,
        Currency.GBP: 0.88,
        Currency.UAH: 38.77,
    }
    GBP = {
        Currency.USD: 1.20,
        Currency.EUR: 1.13,
        Currency.GBP: 1,
        Currency.UAH: 43.94,
    }
    UAH = {
        Currency.USD: 0.027,
        Currency.EUR: 0.026,
        Currency.GBP: 0.023,
        Currency.UAH: 1,
    }

    @classmethod
    def get_rate(cls, currency_from: Currency, currency_to: Currency) -> float:
        """
        Returns the exchange rate between two currencies.

        Args:
            currency_from (Currency): The currency to convert from.
            currency_to (Currency): The currency to convert to.

        Returns:
            float: The exchange rate between the two currencies.
        """

        return cls[currency_from.name].value[currency_to]
