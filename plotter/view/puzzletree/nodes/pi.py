# coding=utf-8

from .simplenode import SimpleNode
from gettext import gettext as _

import math


class Pi(SimpleNode):
    """Node representing pi."""

    CLASS = "pi"
    background = SimpleNode.loadbackground("pi.svg")
    title = _("π")
    description = _(u"Returns the ratio of a circle's circumference to its "
        u"diameter.\n"
        u"π (pi) is approximately 3.14159")

    def __call__(self, x):
        """Returns pi."""
        return math.pi


    def get_equation_string(self, variable):
        """Returns pi, ignoring the variable."""
        return "pi"

