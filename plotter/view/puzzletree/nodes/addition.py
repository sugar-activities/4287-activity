
from .binaryoperator import BinaryOperator as _BinaryOperator
from gettext import gettext as _


class Addition(_BinaryOperator):
    """Addition is a BinaryOperator that adds its two children together."""

    CLASS = "addition"
    background = _BinaryOperator.loadbackground("addition.svg")
    operatorstring = "+"
    title = _("Addition")
    description = _("Combines two objects together into a larger collection."
        " For example, x + x = 2x.")

    def __call__(self, x):
        """Returns self's leftchild(x) + rightchild(x)."""
        return self.children[0](x) + self.children[1](x)

