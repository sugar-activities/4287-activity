from __future__ import absolute_import

import gtk
import cairo
import cairoplot
from .handler import Handler as _Handler

class GTKHandler(_Handler, gtk.DrawingArea):
    """Handler to create plots that output to vector files."""

    def __init__(self, *args, **kwargs):
        """Create Handler for arbitrary surfaces."""
        _Handler.__init__(self)
        gtk.DrawingArea.__init__(self)
       
        # users of this class must set plot manually
        self.plot = None
        self.context = None

        # connect events for resizing/redrawing
        self.connect("expose_event", self.on_expose_event)

    def on_expose_event(self, widget, data):
        """Redraws plot if need be."""
        
        self.context = widget.window.cairo_create()
        if (self.plot is not None):
            self.plot.render()

    def prepare(self, plot):
        """Update plot's size and context with custom widget."""
        _Handler.prepare(self, plot)
        self.plot = plot
        plot.context = self.context

        allocation = self.get_allocation()
        plot.dimensions[cairoplot.HORZ] = allocation.width
        plot.dimensions[cairoplot.VERT] = allocation.height

