"""gtkplotactivity: plotting application not dependent on sugar.
"""

from gettext import gettext as _

import plotter.plot
import plotter.settings
import plotter.view

import gtk

import collections
import os.path
import codecs
import plotter.json as json

# file version info, just in case we break backward compatibility
_FILE_VERSION = 1
_xmin_adjustment = gtk.Adjustment(
    value=-10, step_incr=1, lower=-1e9, upper=1e9)
_xmax_adjustment = gtk.Adjustment(
    value=10, step_incr=1, lower=-1e9, upper=1e9)


class Plotter(gtk.Window):
    """Stand-only gtk window with Plot activity."""

    def __init__(self):
        """Creates a plotter application window."""
        gtk.Window.__init__(self)
        self.connect("delete_event", gtk.main_quit)

        self.init_undo()

        main_vbox = gtk.VBox()
        main_vbox.add_with_properties(self.init_menu(), "expand", False)
        main_vbox.add(self.init_plot())

        main_vbox.show_all()
        self.add(main_vbox)
        self.set_default_size(800, 600)


    def init_menu(self):
        """Creates MenuBar for gtk activity."""
        menu = gtk.MenuBar()

        # file menu
        fileitem = gtk.MenuItem(_("_File"))
        filemenu = gtk.Menu()
        fileitem.set_submenu(filemenu)

        openitem = gtk.MenuItem(_("_Open"))
        openitem.connect("activate", self.on_open)
        filemenu.add(openitem)

        saveitem = gtk.MenuItem(_("_Save"))
        saveitem.connect("activate", self.on_save)
        filemenu.add(saveitem)

        filemenu.add(gtk.SeparatorMenuItem())
        quititem = gtk.MenuItem(_("_Quit"))
        quititem.connect("activate", gtk.main_quit)
        filemenu.add(quititem)
        menu.add(fileitem)

        # edit menu
        edititem = gtk.MenuItem(_("_Edit"))
        editmenu = gtk.Menu()
        edititem.set_submenu(editmenu)

        undoitem = gtk.MenuItem(_("_Undo"))
        undoitem.connect("activate", self.on_undo)
        editmenu.add(undoitem)

        redoitem = gtk.MenuItem(_("_Redo"))
        redoitem.connect("activate", self.on_redo)
        editmenu.add(redoitem)

        editmenu.add(gtk.SeparatorMenuItem())
        copyitem = gtk.MenuItem(_("_Copy"))
        copyitem.connect("activate", self.on_copy)
        editmenu.add(copyitem)

        pasteitem = gtk.MenuItem(_("_Paste"))
        pasteitem.connect("activate", self.on_paste)
        editmenu.add(pasteitem)
        menu.add(edititem)

        return menu


    def init_undo(self):
        """Sets up queues need for undo/redo."""
        self._undo = collections.deque()
        self._redo = collections.deque()


    def init_plot(self):
        """Setup up needed properties for displaying a plot."""

        # make box for equations
        equationbox = gtk.HBox()

        # create input for equations
        self.equations = plotter.view.EquationList(self)
        equationbox.add(self.equations)

        # create button to initiate plot
        plotbutton = gtk.Button(_("Go!"))
        plotbutton.connect("clicked", self.on_plot)
        equationbox.pack_start(plotbutton, expand=False)

        # make box for x-axis configuration
        axisbox = gtk.HBox()
        xminlabel = gtk.Label(_("x min."))
        axisbox.add(xminlabel)
        self.xmin_spin = gtk.SpinButton(_xmin_adjustment)
        axisbox.add(self.xmin_spin)
        xmaxlabel = gtk.Label(_("x max."))
        axisbox.add(xmaxlabel)
        self.xmax_spin = gtk.SpinButton(_xmax_adjustment)
        axisbox.add(self.xmax_spin)

        # create canvas for plotting
        self.canvas = None

        # add pieces to ScrolledWindow (so never have too many inputs)
        self.plot_scrolledwindow = gtk.ScrolledWindow()
        self.plot_vbox = gtk.VBox(spacing=2)
        self.plot_vbox.pack_start(equationbox, expand=False)
        self.plot_vbox.pack_start(axisbox, expand=False)
        self.plot_scrolledwindow.add_with_viewport(self.plot_vbox)
        self.plot_scrolledwindow.set_policy(gtk.POLICY_NEVER,
                gtk.POLICY_AUTOMATIC)

        return self.plot_scrolledwindow


    def get_functions(self):
        """Gets model from equations list."""
        return self.equations.get_model()


    def on_plot(self, widget, data=None):
        """Tells self to draw a plot."""
        self.plot()


    def plot(self):
        """Draws a plot from points."""
        if self.canvas is not None:
            self.plot_vbox.remove(self.canvas)

        self.canvas = plotter.plot.CairoPlotCanvas.fromapp(self)
        self.canvas.show()
        self.plot_vbox.pack_end(self.canvas, True, True)


    def on_save(self, widget, data=None):
        save_popup = gtk.FileChooserDialog(title=_("Save.."),
                action=gtk.FILE_CHOOSER_ACTION_SAVE,
                buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        save_popup.set_default_response(gtk.RESPONSE_OK)

        response = save_popup.run()

        if response == gtk.RESPONSE_OK:
            # write settings to selected file
            # TODO: catch possible exceptions and log error
            filename = save_popup.get_filename()
            self.write_file(filename)

        save_popup.destroy()


    def write_file(self, file_path):
        """Writes settings to a file."""

        # TODO: document possible errors that can occur
        fp = codecs.open(file_path, "w", "utf-8")
        settings = {
            "version": _FILE_VERSION,
            "plot_config": plotter.settings.PlotSettings.fromapp(self).save(),
            "equations": self.equations.save()
        }
        json.dump(settings, fp)


    def on_open(self, widget, data=None):
        open_popup = gtk.FileChooserDialog(title=_("Open.."),
                action=gtk.FILE_CHOOSER_ACTION_OPEN,
                buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        open_popup.set_default_response(gtk.RESPONSE_OK)

        response = open_popup.run()

        if response == gtk.RESPONSE_OK:
            filename = open_popup.get_filename()
            self.read_file(filename)

        open_popup.destroy()


    def read_file(self, file_path):
        """Loads settings from a file."""

        # TODO: document possible errors that can occur
        fp = codecs.open(file_path, "r", "utf-8")
        settings = json.load(fp)

        # TODO: throw appropriate exception here?
        if settings["version"] > _FILE_VERSION:
            return

        # load setting and equations
        plotter.settings.PlotSettings.load(settings["plot_config"]).toapp(self)
        self.equations.load(settings["equations"])

        # make sure graph is shown
        self.plot()


    def register_action(self, action, inverse):
        """Adds an action and its inverse to the undo stack."""
        self._undo.append((action, inverse))
        self._redo.clear()


    def on_undo(self, widget, data=None):
        """Undoes the last actition performed."""

        if len(self._undo) != 0:
            action = self._undo.pop()
            action[1]()
            self._redo.append(action)


    def on_redo(self, widget, data=None):
        """Redoes the last actition undone."""

        if len(self._redo) != 0:
            action = self._redo.pop()
            action[0]()
            self._undo.append(action)


    def _get_focus_widget(self, widget):
        """Gets the widget that is a child of parent with the focus."""
        if widget.flags() & gtk.HAS_FOCUS:
            return widget

        # get currently focused child (get_focus_child requires gtk 2.14)
        focus = None
        if hasattr(widget, "get_children"):
            for child in widget.get_children():
                focus = self._get_focus_widget(child)
                if focus is not None:
                    break
        return focus


    def on_copy(self, widget, data=None):
        """Copies currently selected text."""
        focus = self._get_focus_widget(self.plot_vbox)
        if focus is not None and hasattr(focus, "copy_clipboard"):
            focus.copy_clipboard()


    def on_paste(self, widget, data=None):
        """Pastes text from Clipboard."""
        focus = self._get_focus_widget(self.plot_vbox)
        if focus is not None and hasattr(focus, "paste_clipboard"):
            focus.paste_clipboard()


if __name__ == '__main__':
    # set default icon for the application
    gtk.window_set_default_icon_from_file(os.path.join(
        "data", "icons", "plot-gtk.png"))

    # run standalone application
    app = Plotter()
    app.show_all()
    gtk.main()

