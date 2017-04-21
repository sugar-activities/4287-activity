"""Base class for all nodes (or at least nodes that aren't extremely wierd)."""

import gtk.gdk
import os.path

_FILE_VERSION = 1
NODE_WIDTH = 32
NODE_HEIGHT = 32


class Node(object):
    """Node is a piece of an equation."""

    title = "Node"
    description = "Element of a function."

    # a list of (tile, constructor, getvalue) for nodes w/ params
    parameters = []

    def __init__(self):
        """Initialize children property, since all nodes will need it."""
        self.children = []


    @staticmethod
    def load(settings):
        """Loads a node from a dictionary."""

        if settings is None or settings["version"] > _FILE_VERSION:
            return None

        # this import is here to prevent cyclic imports
        from ..nodes import CLASSES

        # load input view from specified class
        node = CLASSES[settings["class"]].load(settings["settings"])
        node.children = [Node.load(c) for c in settings["children"]]
        return node


    def save(self):
        """Creates dictionary representing current state.

        In dictionary, settings is reserved for sub-classes with
        parameters (like value in Constant).
        """

        settings = {
            "version": _FILE_VERSION,
            "class": self.CLASS,
            "settings": None,
            "children": [None if c is None else c.save()
                for c in self.children]
        }
        return settings


    @staticmethod
    def loadbackground(filename):
        """Loads an image from the puzzle piece folder."""
        return gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join("data", "puzzle", filename),
            NODE_WIDTH, NODE_HEIGHT)


    @staticmethod
    def get_equation_string(node, variable):
        """Returns equation string for node (even when null)."""
        if node is None:
            return ""
        return node.get_equation_string(variable)


    def draw(self, context):
        """Draws puzzle piece at current location on context."""

        # TODO: draw piece background as well (like a puzzle piece)

        # draw image representing the node type
        context.set_source_pixbuf(self.background, 0, 0)
        context.paint()

