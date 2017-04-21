# coding=utf-8

from .simplenode import SimpleNode
from gettext import gettext as _

import math


class E(SimpleNode):
    """Node representing e."""

    CLASS = "e"
    background = SimpleNode.loadbackground("e.svg")
    title = _("e")
    description = _(u"e is an irrational number such that the derivative "
            u"of f(x) = e ** x is f(x).\n"
            u"e is approximately 2.71828")

    def __call__(self, x):
        """Returns e."""
        return math.e


    def get_equation_string(self, variable):
        """Returns e, ignoring the variable."""
        return "e"

