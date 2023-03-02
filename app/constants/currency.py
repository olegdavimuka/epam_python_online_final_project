"""
This module contains the Currency enumeration class that
represents the currencies supported in the application.

Dependencies:
    - enum.Enum (built-in)
    - enum.unique (built-in)

Exported Classes:
    - Currency: An enumeration of currencies supported in the application.

"""

from enum import Enum, unique


@unique
class Currency(Enum):
    """
    The Currency enumeration class represents the currencies supported in the application.

    Enum Members:
        - USD (str): The US dollar.
        - EUR (str): The Euro.
        - GBP (str): The British pound.
        - UAH (str): The Ukrainian hryvnia.

    """

    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    UAH = "UAH"
