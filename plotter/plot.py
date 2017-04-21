"""Methods for creating plot figures."""

import cairoplot
from cairoplot.handlers.gtk import GTKHandler

class CairoPlotCanvas(GTKHandler):
    """GTK canvas displaying plots from."""

    @staticmethod
    def fromapp(app):
        """Creates a CairoPlotCanvas from application."""

        # plotsettings = plotter.settings.PlotSettings.fromapp(self)
        xmin = app.xmin_spin.get_value()
        xmax = app.xmax_spin.get_value()
        xstep = (xmax - xmin) / 100.0

        canvas = CairoPlotCanvas()

        # get data (functions in a list)
        functions = app.get_functions()

        # create plot
        plot = cairoplot.FunctionPlot(canvas, data=functions,
                x_bounds=(xmin, xmax), step=xstep,
                width=500, height=500, background="white",
                border=20, axis=True, grid=True)
        canvas.plot = plot

        return canvas

