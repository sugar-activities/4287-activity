
from .simplenode import SimpleNode
from gettext import gettext as _


class AbsoluteValue(SimpleNode):
    """Node representing the absolute value function: f(x) = abs(x)."""

    CLASS = "absolutevalue"
    background = SimpleNode.loadbackground("absolutevalue.svg")
    title = _("Absolute Value")
    description = _(u"Returns the distance a value is from zero.\n"
        u"For example, f(-3) = 3 and f(3) = 3.")

    def __call__(self, x):
        """Calls the absolute value function."""
        return abs(x)


    def get_equation_string(self, variable):
        """Returns abs(x) given variable, x."""
        return "abs(%s)" % variable

