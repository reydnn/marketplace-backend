from rest_framework.exceptions import ParseError


class OrderBadRequest(ParseError):
    """400 ошибка при создании заказа"""
