"""Module for code-defined view objects.

WARNING: do NOT put business logic in here.
Classes needing logic should use corresponding data models via
get_model(), load_model() methods.
"""

import gtk
from gettext import gettext as _

from .equation import EquationInput as _EquationInput
from .puzzletree import PuzzleInput as _PuzzleInput

# just in case we break backward compatibility
_FILE_VERSION = 1
_EQUATION_VERSION = 1


class EquationList(gtk.HBox):
    """A list of equations."""

    def __init__(self, app):
        """Creates it..."""
        gtk.HBox.__init__(self)

        # save application instance for undo/redo
        self.app = app

        # create box for equation inputs
        self.vbox = gtk.VBox()
        self.vbox.show()
        self.pack_start(self.vbox)

        # create add button for multiple equations
        imagevbox = gtk.VBox()
        addimage = gtk.Image()
        addimage.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_BUTTON)
        addbutton = gtk.Button()
        addbutton.add(addimage)
        addbutton.show()
        imagevbox.pack_end(addbutton, expand=False, fill=False)
        imagevbox.show()
        self.pack_start(imagevbox, expand=False)
        addbutton.connect("clicked", self._on_add, None)

        # created default equation input
        self._equations = []
        self._add_equation(_PuzzleInput(app))


    def save(self):
        """Returns dictionary to be used in saving JSON."""

        # create list of equations
        equations_settings = []
        for equation in self._equations:
            equations_settings.append(self._saveequation(equation))

        settings = {
            "version": _FILE_VERSION,
            "equations": equations_settings
        }

        return settings


    def _saveequation(self, equation):
        """Creates dictionary to save state of an equation."""

        return {
            "version": _EQUATION_VERSION,
            "class": equation.CLASS,
            "settings": equation.save()
        }


    def load(self, settings):
        """Updates view with equations loaded from settings."""

        if settings["version"] > _FILE_VERSION:
            return

        # remove all existing equations
        self.clear()

        # create new equations from settings
        for equation in settings["equations"]:
            self._loadequation(equation)


    def _loadequation(self, equation):
        """Loads an equation from saved state."""

        if equation["version"] > _EQUATION_VERSION:
            return

        # load input view from specified class
        loaded = _VIEW_CLASSES[equation["class"]].load(
                        self.app, equation["settings"])
        loaded_input = self._add_equation(loaded)
        return (loaded, loaded_input)


    def get_model(self):
        """Returns a list of equations."""

        equations = []
        for equation in self._equations:
            equations.append(equation.get_model())
        return equations


    def _register_addremove(self, equation, equation_input, isadding=False):
        """Register an add/remove equation action."""

        # create actions (which preserve equation order)
        i = self._equations.index(equation)
        def remove():
            self._remove_equation(equation, equation_input)
        def add():
            self._insert_equation_input(i, equation, equation_input)

        # register the action (inverse switched for adding vs removing)
        action = remove
        inverse = add
        if isadding:
            action = add
            inverse = remove
        self.app.register_action(action, inverse)


    def _on_add(self, widget, data=None):
        """Event to add a new equation input."""

        # add a new equation
        equation = _PuzzleInput(self.app)
        equation_input = self._add_equation(equation)

        # register the action for undo/redo
        self._register_addremove(equation, equation_input, isadding=True)


    def _on_remove(self, widget, equation, equation_input):
        """Event to remove an equation."""
        self._register_addremove(equation, equation_input, isadding=False)
        self._remove_equation(equation, equation_input)


    def _remove_equation(self, equation, equation_input):
        """Removes an equation from the list."""
        self._equations.remove(equation)
        self.vbox.remove(equation_input)


    def _add_equation_input(self, equation, equation_input):
        """Adds an equation to the end of the list."""
        self._equations.append(equation)
        self.vbox.pack_start(equation_input, expand=False)


    def _insert_equation_input(self, i, equation, equation_input):
        """Inserts an equation to the list at position i."""
        self._equations.insert(i, equation)
        self.vbox.pack_start(equation_input, expand=False)
        self.vbox.reorder_child(equation_input, i)


    def _convert_equation(self, equation, equation_input):
        """Converts an equation into a Python input."""

        # create new control with python equation text
        i = self._equations.index(equation)
        equationstring = equation.get_equation_string()
        pythonequation = _EquationInput(self.app, equationstring)
        pythonequation_input = self._create_equation(pythonequation)

        # register the action (for undo/redo)
        def inverse():
            self._remove_equation(pythonequation, pythonequation_input)
            self._insert_equation_input(i, equation, equation_input)
        def action():
            self._remove_equation(equation, equation_input)
            self._insert_equation_input(i, pythonequation, pythonequation_input)
        self.app.register_action(action, inverse)
        action()


    def _create_equation(self, equation):
        """Creates input for equation without adding it to the list."""

        # can only convert equation inputs that have equation string conversion
        canconvert = hasattr(equation, "get_equation_string")

        # create remove button
        equation_input = gtk.HBox()
        removeimage = gtk.Image()
        removeimage.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_BUTTON)
        removebutton = gtk.Button()
        removebutton.add(removeimage)
        removebutton.show_all()
        equation_input.pack_start(removebutton, expand=False)
        equation_input.pack_start(equation)

        # connect button click to remove equation
        removebutton.connect("clicked", self._on_remove, equation,
                equation_input)

        # create convert to text button
        if canconvert:
            convertbutton = gtk.Button(_("To Python"))
            convertbutton.show_all()
            equation_input.pack_start(convertbutton, expand=False)

            def convertequation(widget, data=None):
                self._convert_equation(equation, equation_input)
            convertbutton.connect("clicked", convertequation)

        # display equation input
        equation_input.show()
        return equation_input


    def _add_equation(self, equation):
        """Adds an equation to the list."""
        # display equation input
        equation_input = self._create_equation(equation)
        self._add_equation_input(equation, equation_input)
        return equation_input


    def clear(self):
        """Removes all equations from view."""
        self.vbox.foreach(self.vbox.remove)
        self._equations = []



# dictionary of all input view classes
_VIEW_CLASSES = {
    _EquationInput.CLASS: _EquationInput,
    _PuzzleInput.CLASS: _PuzzleInput
}

