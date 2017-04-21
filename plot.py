
from gtkplotactivity import Plotter

import gtk
from sugar.activity import activity
from gettext import gettext as _


class PlotActivity(activity.Activity):
    def __init__(self, handle):
        """Creates a plotter application window."""
        activity.Activity.__init__(self, handle)

        # create toolbox: this provides default sugar controls
        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        # setup container for glade widgets
        main_view = gtk.VBox()

        # load Glade XML and get main window
        # get the VBox that's a child of the glade window
        self._app = app = Plotter()
        app.plot_scrolledwindow.reparent(main_view)
        app.plot_scrolledwindow.show()

        # create edit toolbar
        edit_toolbar = activity.EditToolbar()
        toolbox.add_toolbar(_("Edit"), edit_toolbar)
        edit_toolbar.show()

        # connect undo/redo to app events
        edit_toolbar.undo.connect("clicked", app.on_undo)
        edit_toolbar.redo.connect("clicked", app.on_redo)
        edit_toolbar.copy.connect("clicked", app.on_copy)
        edit_toolbar.paste.connect("clicked", app.on_paste)

        # make main_view act as our canvas
        main_view.show()
        self.set_canvas(main_view)
        self.show_all()


    def write_file(self, file_path):
        """Tells application to write to file."""
        self._app.write_file(file_path)

    def read_file(self, file_path):
        """Tells application to load from file."""
        self._app.read_file(file_path)

