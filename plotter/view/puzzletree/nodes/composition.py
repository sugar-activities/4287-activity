# coding=utf-8

from .node import Node
from .binaryoperator import BinaryOperator
from gettext import gettext as _


class Composition(BinaryOperator):
    """Composition: left compose right function."""

    CLASS = "composition"
    background = BinaryOperator.loadbackground("composition.svg")
    title = _("Function Composition")
    description = _(u"Combines two functions by applying the result of the "
        u"right function to the left.\n"
        u"For example, (x ** 2) ∘ (x + 1) = (x + 1) ** 2.")

    def __call__(self, x):
        """Returns self's leftchild(rightchild(x))."""
        return self.children[0](self.children[1](x))


    def get_equation_string(self, variable):
        """Returns a string representing the current equation."""

        # result from right will be new variable in left
        variable = Node.get_equation_string(self.children[1], variable)
        return Node.get_equation_string(self.children[0], variable)

