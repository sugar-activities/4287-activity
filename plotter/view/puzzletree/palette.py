
from . import nodes

import gtk



class PuzzlePalette(gtk.VBox):
    """PuzzlePalette has buttons for adding nodes to function tree."""

    def __init__(self, app, display):
        """Create a palette of nodes to use in making funtions.

        Parameters
        ==========

        :display: PuzzleDisplay that contains the function tree.
        """
        gtk.VBox.__init__(self, spacing=8)

        self.app = app
        self._display = display

        # make buttons for operators
        isfirstcategory = True
        for title, category in nodes.CATEGORIES:
            # create label for title
            titlelabel = gtk.Label("<big>%s</big>" % title)
            titlelabel.set_use_markup(True)
            self.pack_start(titlelabel)

            # add nodes to category palette
            for node in category:
                nodebox = gtk.HBox()

                # create button with node image
                # (also, create a vbox, so its not stretched out)
                imagevbox = gtk.VBox()
                nodeimage = gtk.Image()
                nodeimage.set_from_pixbuf(node.background)
                nodebutton = gtk.Button()
                nodebutton.add(nodeimage)
                imagevbox.pack_start(nodebutton, expand=False, fill=False)
                nodebox.pack_start(imagevbox, expand=False)

                # add labels for title and description
                descrbox = gtk.VBox()

                # title (align left)
                nodetitlelabel = gtk.Label(node.title)
                nodetitlelabel.set_alignment(0.02, 0.0)
                descrbox.pack_start(nodetitlelabel, padding=1)

                # (optional) parameters for node
                parameterfetchers = []
                totalparameters = len(node.parameters)
                if totalparameters != 0:
                    paramtable = gtk.Table(totalparameters, 2)
                    descrbox.pack_start(paramtable)

                    for row, paramvalue in enumerate(node.parameters):
                        paramtitle, paramclass, paramvalue = paramvalue

                        # parameter title label
                        paramlabel = gtk.Label(paramtitle)
                        paramtable.attach(paramlabel, 0, 1, row, row + 1)

                        # parameter input
                        paraminput = paramclass()
                        paramtable.attach(paraminput, 1, 2, row, row + 1)

                        # add method to get parameter to parameterfetchers
                        parameterfetchers.append((paramvalue, paraminput))

                # description (align mostly left)
                descrlabel = gtk.Label(node.description)
                descrlabel.set_line_wrap(True)
                descrlabel.set_alignment(0.1, 0.0)
                descrbox.pack_start(descrlabel)
                nodebox.pack_start(descrbox)

                # connect click event to add node
                nodebutton.connect("clicked", self.on_add_event, node,
                        *parameterfetchers)
                self.pack_start(nodebox, padding=1)


    def addnode(self, node):
        """Adds node to display."""

        def action():
            # add node and hide palette if no more nodes can be added
            self._display.addnode(node)
            if self._display.nextnode is None:
                self.hide()
        def inverse():
            self._display.undo()
            self.show_all()
        self.app.register_action(action, inverse)

        # actually add the node
        action()


    def on_add_event(self, widget, nodeclass, *args):
        """Adds node of type nodeclass to display."""
        self.addnode(nodeclass(*[v(p) for v, p in args]))

