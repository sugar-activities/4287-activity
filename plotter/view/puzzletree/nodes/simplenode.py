
from .node import Node as _Node


class SimpleNode(_Node):
    """Nodes with no parameters, so load just uses default constructor."""

    @classmethod
    def load(nodeclass, settings):
        """Ignore settings, since no parameters for SimpleNode."""
        return nodeclass()

