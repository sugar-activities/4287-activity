
from .binaryoperator import BinaryOperator as _BinaryOperator
from gettext import gettext as _


class Exponentiation(_BinaryOperator):
    """Exponentiation: a BinaryOperator for powers."""

    CLASS = "exponentiation"
    background = _BinaryOperator.loadbackground("exponentiation.svg")
    operatorstring = "**"
    title = _("Exponentiation")
    description = _(u"Combines two objects by multiplying the left one "
        u"for the right number of times.\n"
        u"For example, x ** 2 = x * x.")

    def __call__(self, x):
        """Returns self's leftchild(x) ** rightchild(x)."""
        return self.children[0](x) ** self.children[1](x)

