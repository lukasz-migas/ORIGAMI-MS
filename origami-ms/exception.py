# -*- coding: utf-8 -*-
# __author__ lukasz.g.migas
from dialogs import dlgBox


class MessageError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error

    Usage:
        raise MessageError("Title", "Message")
    """

    def __init__(self, title, message):
        self.title = title
        self.message = message

        dlgBox(title, message, type="Error")
