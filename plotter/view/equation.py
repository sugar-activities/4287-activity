"""Widgets for equation input."""

from gettext import gettext as _
import gtk
import plotter.parse


_FILE_VERSION = 1


class EquationInput(gtk.HBox):
    """A text box..."""

    # unique identifier for this input type
    CLASS = "text"

    def __init__(self, app, equation="x"):
        """Creates input..."""
        gtk.HBox.__init__(self)

        # add f(x) rather than y, to imply this is a function
        self.pack_start(gtk.Label(_("f(x) =")), expand=False,
                padding=5)

        # create equation entry w/ default text
        self._equation = gtk.Entry()
        self._equation.set_text(equation)
        self.pack_start(self._equation)
        self.show_all()


    @staticmethod
    def load(app, settings):
        """Creates new equation entry from saved state."""

        if settings["version"] > _FILE_VERSION:
            return EquationInput(app)
        return EquationInput(app, settings["text"])


    def save(self):
        """Returns settings dictionary with current state."""

        settings = {
            "version": _FILE_VERSION,
            "text": self._equation.get_text()
        }
        return settings


    def get_model(self):
        """Returns function with entry."""
        return plotter.parse.parse(self._equation.get_text())

