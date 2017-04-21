from .node import Node as _Node


class BinaryOperator(_Node):
    """BinaryOperators have at most two children."""

    def __init__(self, leftchild=None, rightchild=None):
        """Create binary operator (possibly with children)."""
        _Node.__init__(self)
        self.children = [leftchild, rightchild]


    @classmethod
    def load(nodeclass, settings):
        """Creates a new BinaryOperator of type nodeclass.

        Default BinaryOperators don't have any parameters,
        so this just returns a new node.
        """
        return nodeclass()


    def get_equation_string(self, variable):
        """Returns a string representing the current equation."""

        return "(%s %s %s)" % (
            _Node.get_equation_string(self.children[0], variable),
            self.operatorstring,
            _Node.get_equation_string(self.children[1], variable))

