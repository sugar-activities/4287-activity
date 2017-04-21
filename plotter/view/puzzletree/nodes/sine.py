
from .simplenode import SimpleNode
from gettext import gettext as _

import math


class Sine(SimpleNode):
    """Node representing the sine function: f(x) = sin(x)."""

    CLASS = "sine"
    background = SimpleNode.loadbackground("sine.svg")
    title = _("Sine")
    description = _(u"Returns the ratio of the length of a side opposite an "
        u"acute angle in a right trianale to the length of the hypotenuse.\n"
        u"For example, sin(pi / 4) = 1 / sqrt(2)")

    def __call__(self, x):
        """Calls the sine function."""
        return math.sin(x)


    def get_equation_string(self, variable):
        """Returns sin(x) given x."""
        return "sin(%s)" % variable

