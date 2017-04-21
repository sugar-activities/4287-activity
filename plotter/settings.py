"""Objects for keeping track of graph settings."""

# version of settings (in case we break backward compatibility)
_FILE_VERSION = 1


class PlotSettings(object):
    """Settings for displaying a plot."""

    def __init__(self, xmin, xmax):
        """Saves settings."""

        self.xmin = xmin
        self.xmax = xmax

    @classmethod
    def fromapp(settingsclass, app):
        """Loads settings from a Plotter application."""

        xmin = app.xmin_spin.get_value()
        xmax = app.xmax_spin.get_value()

        return settingsclass(xmin, xmax)

    @classmethod
    def load(settingsclass, settings):
        """Loads settings from a file created by write()."""

        # TODO: throw exception for old versions
        if settings["version"] > _FILE_VERSION:
            return settingsclass(0, 0)

        xmin = settings["xmin"]
        xmax = settings["xmax"]

        return settingsclass(xmin, xmax)


    def save(self):
        """Returns serialized version of settings as dictionary."""

        return {
            "version": _FILE_VERSION,
            "xmin": self.xmin,
            "xmax": self.xmax,
        }


    def toapp(self, app):
        """Makes application reflect values from settings."""

        app.xmin_spin.set_value(self.xmin)
        app.xmax_spin.set_value(self.xmax)


