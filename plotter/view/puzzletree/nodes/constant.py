
from .node import Node as _Node
from gettext import gettext as _

import gtk

_FILE_VERSION = 1

# default values for editing the constant parameter
_constant_adjustment = gtk.Adjustment(
    value=2, step_incr=1, lower=-1e9, upper=1e9)

def _create_constant_spin():
    """Creates spin button for changing constant's value."""
    return gtk.SpinButton(_constant_adjustment,
        climb_rate=1, digits=2)



class Constant(_Node):
    """Constant represent constant real-number values."""

    CLASS = "constant"
    background = _Node.loadbackground("constant.svg")
    title = _("Constant")
    description = _(u"Returns the same value, ignoring the input.\n"
            "For example, f(x) = 2.")

    parameters = [
        (_("Value"), _create_constant_spin, gtk.SpinButton.get_value)
    ]

    def __init__(self, value=2):
        """Create Constant with value of value."""
        _Node.__init__(self)
        self.value = value


    def __call__(self, x):
        """Ignore the parameter and return a constant value."""
        return self.value


    @staticmethod
    def load(settings):
        """Loads constant from value in dictionary."""
        if settings["version"] > _FILE_VERSION:
            return Constant()
        if "value" in settings:
            return Constant(settings["value"])


    def save(self):
        """Saves constant to a dictionary."""
        headersettings = _Node.save(self)
        settings = {
            "version": _FILE_VERSION,
            "value": self.value
        }
        headersettings["settings"] = settings
        return headersettings


    def get_equation_string(self, variable):
        """Returns string form of value (ignoring variable)."""
        return str(self.value)

