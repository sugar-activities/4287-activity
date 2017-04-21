
import math
import copy


# create list of "safe" methods to allow in equations
_safe_dict = {
    "__builtins__": {"__import__": __import__},
    "abs": abs,
}

# grab desired methods from math library
_math_funcs = ['ceil', 'floor',
    'exp', 'log', 'log10', 'pow', 'sqrt',
    'acos', 'asin', 'atan', 'atan2', 'cos', 'hypot', 'sin', 'tan',
    'cosh', 'sinh', 'tanh',
    'pi', 'e'
]
for symbol in _math_funcs:
    _safe_dict[symbol] = getattr(math, symbol)


def parse(stringfunc):
    """Returns a method corresponding to stringfunc."""

    # create a function using user input as the return line
    stringfunction = ("from __future__ import division\n"
        "del __builtins__['__import__']\n"
        "def plot(x):\n"
        "    return %s"
        % stringfunc.replace("^", "**"))
    compiledfunction = compile(stringfunction, "<string>", "exec")

    # plot the method using "safe" globals and locals
    # http://lybniz2.sourceforge.net/safeeval.html
    # this should also be thread-safe (I think...)
    globalscopy = copy.deepcopy(_safe_dict)
    localscopy = {}
    exec compiledfunction in globalscopy, localscopy
    return localscopy["plot"]

