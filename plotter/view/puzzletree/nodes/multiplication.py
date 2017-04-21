
from .binaryoperator import BinaryOperator as _BinaryOperator
from gettext import gettext as _


class Multiplication(_BinaryOperator):
    """Multiplication is a BinaryOperator that multiplies its two children."""

    CLASS = "multiplication"
    background = _BinaryOperator.loadbackground("multiplication.svg")
    operatorstring = "*"
    title = _("Multiplication")
    description = _(u"Combines two objects by adding the left one "
        u"for the right number of times.\n"
        u"For example, x * 3 = x + x + x.")

    def __call__(self, x):
        """Returns self's leftchild(x) * rightchild(x)."""
        return self.children[0](x) * self.children[1](x)

