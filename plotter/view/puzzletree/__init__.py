"""Module for mouse function input."""

import gtk

from .display import PuzzleDisplay
from .palette import PuzzlePalette
from .nodes import Node

_FILE_VERSION = 1

class PuzzleInput(gtk.VBox):
    """PuzzleInput is a control that uses mouse input to create functions."""

    CLASS = "puzzle"

    def __init__(self, app, rootnode=None):
        """Creates input (and display) of tree.

        We'd like to support multiple trees for click-and-drag,
        but for now, just one tree is made at a time.
        """
        gtk.VBox.__init__(self)

        self.app = app

        # create box to hold display and undo button
        displaybox = gtk.HBox()
        self.pack_start(displaybox)

        # create display for drawing function tree
        displayscroll = gtk.ScrolledWindow()
        displayscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_NEVER)
        displayview = gtk.Viewport()
        self._display = PuzzleDisplay(rootnode)
        displayview.add(self._display)
        displayscroll.add(displayview)
        displaybox.pack_start(displayscroll)

        # undo button (TODO: this isn't really undo)
        undoimage = gtk.Image()
        undoimage.set_from_stock(gtk.STOCK_UNDO, gtk.ICON_SIZE_BUTTON)
        undobutton = gtk.Button()
        undobutton.add(undoimage)
        undobutton.show_all()
        displaybox.pack_start(undobutton, expand=False)

        # connect undo event (should show palette and undo)
        undobutton.connect("clicked", self.on_undo)

        # create buttons for adding nodes
        palette = PuzzlePalette(app, self._display)
        self.pack_start(palette)
        self._palette = palette

        # hide palette if it cannot be used
        self.show_all()
        if (self._display.rootnode is not None and
            self._display.nextnode is None):
            palette.hide()


    @staticmethod
    def load(app, settings):
        """Create new input from dictionary state."""

        if settings["version"] > _FILE_VERSION:
            return PuzzleInput()
        return PuzzleInput(app, Node.load(settings["settings"]))


    def save(self):
        """Create a dictionary to save current state."""

        nodesettings = None
        if self._display.rootnode is not None:
            nodesettings = self._display.rootnode.save()

        settings = {
            "version": _FILE_VERSION,
            "settings": nodesettings
        }
        return settings


    def on_undo(self, widget, data=None):
        """Undoes the previous action (removes bottom-right node)."""

        removednode = self._display.undo()
        self._palette.show_all()

        # register action for undo/redo
        def action():
            self._display.undo()
            self._palette.show_all()
        def inverse():
            self._display.addnode(removednode)
            if self._display.nextnode is None:
                self._palette.hide()
        self.app.register_action(action, inverse)


    def get_model(self):
        """Returns callable model from the tree."""
        return self._display.get_model()


    def get_equation_string(self):
        """Returns a string representing the current equation."""
        return Node.get_equation_string(self._display.rootnode, "x")

