
import copy
import gtk
import gtk.gdk
import os.path
import bisect

from .nodes import Node, NODE_WIDTH, NODE_HEIGHT

_PAREN_WIDTH = 16
_BINARY_OPERATOR_WIDTH = 2 * _PAREN_WIDTH + 2 * NODE_WIDTH


class PuzzleDisplay(gtk.DrawingArea):
    """Displays graphical representation of function tree."""

    _leftparen = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join("data", "puzzle", "leftparen.svg"),
            _PAREN_WIDTH, NODE_HEIGHT)

    _rightparen = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join("data", "puzzle", "rightparen.svg"),
            _PAREN_WIDTH, NODE_HEIGHT)

    _blank = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join("data", "puzzle", "blank.svg"),
            NODE_WIDTH, NODE_HEIGHT)

    def __init__(self, rootnode=None):
        """Creates a tree, and initializes code for modifying it.

        For now, there is only one spot that new operators/functions
        can be added, and that is the bottom-left-most null pointer.
        """
        gtk.DrawingArea.__init__(self)

        self.rootnode = rootnode
        self._updatenextnode()

        # keep track of all nodes and their positions (for tooltip)
        self._nodes = []
        self._positions = []

        # setup tooltips
        self.set_property("has-tooltip", True)
        self.connect("query-tooltip", self.on_query_tooltip)

        # connect events for resizing/redrawing
        self.connect("expose_event", self.on_expose_event)

        # make sure we have space for the puzzle pieces
        self.width = PuzzleDisplay._getwidth(rootnode)
        self.height = NODE_HEIGHT
        self.set_size_request(self.width, self.height)


    def on_expose_event(self, widget, data):
        """Redraws plot if need be."""
        self.draw(widget.window.cairo_create())


    def on_query_tooltip(self, widget, x, y, keyboard_mode, tooltip, *args):
        """Updates the tooltip based on which node mouse is over."""

        node = self._nodeatposition(x)
        if node is not None:
            # draw tooltip for node under the cursor
            tooltip.set_text(Node.get_equation_string(node, "x"))
        else:
            # draw tooltip for whole tree
            tooltip.set_text(Node.get_equation_string(self.rootnode, "x"))

        return True


    def get_model(self):
        """Returns a copy of the rootnode, which should be callable."""

        # TODO: if tree state is invalid, we shouldn't be calling this
        if self.rootnode is None:
            return lambda x: 0
        return copy.deepcopy(self.rootnode)


    def draw(self, context):
        """Draws the current tree (with next node highlighted).

        Draws from left-to-right, so it walks the node tree depth-first.
        """

        # reset position list
        self._nodes = []
        self._positions = []

        # draw the tree (and update position list)
        context.save()
        self._drawtree(self.rootnode, context)
        context.restore()


    @staticmethod
    def _getwidth(node):
        """Returns desired width for drawing tree rooted at node."""

        # just on piece
        if node is None or len(node.children) == 0:
            return NODE_WIDTH

        # make room for parentheses on binary operators
        nodewidth = NODE_WIDTH
        if len(node.children) == 2:
            nodewidth += _PAREN_WIDTH * 2

        for c in node.children:
            nodewidth += PuzzleDisplay._getwidth(c)
        return nodewidth


    @staticmethod
    def _drawparen(paren, context):
        """Draws a parenthesis and translates by correct amount."""
        context.set_source_pixbuf(paren, 0, 0)
        context.paint()
        context.translate(_PAREN_WIDTH, 0)


    def _drawtree(self, node, context, isfirstblank=True):
        """Draws the tree rooted at node from left-to-right.

        Returns True if no blank has yet been drawn, else False.
        """

        # for empty nodes, just translate to right
        # if it is the first empty node that we're drawing,
        #  indicate visually that this is where the next node will be
        if node is None:
            if isfirstblank:
                context.set_source_pixbuf(PuzzleDisplay._blank, 0, 0)
                context.paint()
            context.translate(NODE_WIDTH, 0)
            return False

        # unary operators, binary operators, and leaves are drawn differently
        totalchildren = len(node.children)

        def drawnode():
            """After each draw, translate by node width."""

            # keep track of all nodes and their positions (for tooltip)
            self._nodes.append(node)
            matrix = context.get_matrix()
            self._positions.append(matrix[4])

            # draw node and move to next place
            node.draw(context)
            context.translate(NODE_WIDTH, 0)

        if totalchildren == 2:
            # draw parentheses around all BinaryOperators
            PuzzleDisplay._drawparen(PuzzleDisplay._leftparen, context)

            # BinaryOperator
            # draw left-most child first, then node, then right child
            isfirstblank = self._drawtree(
                node.children[0], context, isfirstblank)
            drawnode()
            isfirstblank = self._drawtree(
                node.children[1], context, isfirstblank)

            PuzzleDisplay._drawparen(PuzzleDisplay._rightparen, context)

        elif totalchildren == 1:
            # UnaryOperator
            # operator gets drawn first (e.g. -x)
            drawnode()
            isfirstblank = self._drawtree(
                node.children[0], context, isfirstblank)

        else:
            drawnode()

        return isfirstblank


    def addnode(self, node):
        """Adds node to appropriate location."""

        # make it the root of the tree if no root exists
        if self.rootnode is None:
            self.rootnode = node

        # no open slots for adding nodes exist
        elif self.nextnode is None:
            return

        # add to left-most empty slot in nextnode
        else:
            for i in range(len(self.nextnode.children)):
                if self.nextnode.children[i] is None:
                    self.nextnode.children[i] = node
                    break

        # calculate desired width as we add pieces
        # new size is based on how many blank spaces are added
        totalblanks = len(node.children)
        if totalblanks != 0:
            if totalblanks == 2:
                # BinaryOperators need space for two blanks and parentheses
                self.width += _BINARY_OPERATOR_WIDTH
            else:
                # UnaryOperators just need space for one blank
                self.width += NODE_WIDTH
            self.set_size_request(self.width, self.height)

        # refresh the view, since the tree has changed
        self._updatenextnode()
        self.queue_draw()


    def undo(self):
        """Removes the node that was last added."""

        # can't undo anymore if the tree is empty
        if self.rootnode is None:
            return

        # find parent of node to remove
        lastparent = PuzzleDisplay._findlastnode(self.rootnode)

        # determine which node are we removing and remove it
        removednode = None
        if lastparent is None:
            removednode = self.rootnode
            self.rootnode = None
        else:
            # find right-most child
            for nodeindex in reversed(range(len(lastparent.children))):
                node = lastparent.children[nodeindex]
                if node is not None:
                    lastparent.children[nodeindex] = None
                    removednode = node
                    break

        # calculate desired width as we remove pieces
        # new size is based on how many blank spaces are removed
        totalblanks = len(removednode.children)
        if totalblanks != 0:
            if totalblanks == 2:
                # BinaryOperators need space for two blanks and parentheses
                self.width -= _BINARY_OPERATOR_WIDTH
            else:
                # UnaryOperators just need space for one blank
                self.width -= NODE_WIDTH
            self.set_size_request(self.width, self.height)

        # refresh the view, since the tree has changed
        self._updatenextnode()
        self.queue_draw()
        return removednode


    def _updatenextnode(self):
        """Sets next pointer to bottom-left-most node with null child."""

        # if no nodes in tree, next should create rootnode
        self.nextnode = None
        if self.rootnode is None:
            return

        # do depth-first search to find bottom-left-most node
        self.nextnode = PuzzleDisplay._findnullchild(self.rootnode)


    def _nodeatposition(self, x):
        """Returns node at position, x, or None if no node is there."""

        nodeindex = bisect.bisect(self._positions, x) - 1
        if nodeindex >= 0 and NODE_WIDTH > x - self._positions[nodeindex]:
            return self._nodes[nodeindex]
        return None


    @staticmethod
    def _findnullchild(node):
        """Finds first node that has a null child.

        Returns bottom-left-most node with null child or
            None if no such nodes are in the tree."""

        for child in node.children:
            # does this node have a null child
            if child is None:
                return node

            bottomleft = PuzzleDisplay._findnullchild(child)
            if bottomleft is not None:
                return bottomleft

        # no nodes with null children
        return None


    @staticmethod
    def _findlastnode(node):
        """Finds bottom-right-most node in the tree.

        Returns parent of bottom-rigth-most node or
            None if node has no children."""

        for child in reversed(node.children):
            # don't traverse null children
            if child is None:
                continue

            lastparent = PuzzleDisplay._findlastnode(child)
            if lastparent is None:
                return node
            else:
                return lastparent

        # this node is not the parent of any nodes
        return None

