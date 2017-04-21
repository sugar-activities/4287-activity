"""All possible nodes that can be created are listed here."""

# group nodes into types (operators & functions)
# operators
from .addition import Addition
from .composition import Composition
from .exponentiation import Exponentiation
from .multiplication import Multiplication

OPERATORS = [
    Addition,
    Multiplication,
    Exponentiation,
    Composition
]

# constants
from .constant import Constant
from .pi import Pi
from .e import E

CONSTANTS = [
    Pi,
    E,
    Constant,
]

# functions
from .identity import Identity
from .absolutevalue import AbsoluteValue
from .sine import Sine

FUNCTIONS = [
    Identity,
    AbsoluteValue,
    Sine,
]

# list categories in the order they should be displayed
from gettext import gettext as _
CATEGORIES = [
    (_("Operators"), OPERATORS),
    (_("Functions"), FUNCTIONS),
    (_("Constants"), CONSTANTS),
]

# generate class list for loading from a dictionary
from itertools import chain as _chain

CLASSES = {}
for node in _chain(*(c[1] for c in CATEGORIES)):
    CLASSES[node.CLASS] = node

# get this last, since they aren't nodes we can make
from .node import Node, NODE_WIDTH, NODE_HEIGHT

