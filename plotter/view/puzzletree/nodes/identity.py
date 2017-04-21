
from .simplenode import SimpleNode
from gettext import gettext as _


class Identity(SimpleNode):
    """Node representing the identity function: f(x) = x."""

    CLASS = "identity"
    background = SimpleNode.loadbackground("identity.svg")
    title = _("Identity")
    description = _(u"Returns whatever was input to it.\n"
        u"For example, f(x) = x.")

    def __call__(self, x):
        """Identity function (f(x) = x)."""
        return x


    def get_equation_string(self, variable):
        """Returns variable, since this is the identity function."""
        return variable

