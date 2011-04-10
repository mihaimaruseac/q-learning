# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import gtk
import glib

import config
import world
import plot

from globaldefs import *

def initImages():
    """
    Init's the images. It stays here instead of being placed in globaldefs.py
    because it needs gtk imported.
    """
    i = gtk.Image()
    i.set_from_file(VOID_FILE)
    IMAGES[VOID] = i.get_pixbuf()
    i.set_from_file(EMPTY_FILE)
    IMAGES[EMPTY] = i.get_pixbuf()
    i.set_from_file(ROBOT_FILE)
    IMAGES[ROBOT] = i.get_pixbuf()
    i.set_from_file(ROBOT_N_FILE)
    IMAGES[ROBOT_N] = i.get_pixbuf()
    i.set_from_file(ROBOT_E_FILE)
    IMAGES[ROBOT_E] = i.get_pixbuf()
    i.set_from_file(ROBOT_S_FILE)
    IMAGES[ROBOT_S] = i.get_pixbuf()
    i.set_from_file(ROBOT_W_FILE)
    IMAGES[ROBOT_W] = i.get_pixbuf()

class MainWindow(gtk.Window):
    """
    Holds the definition for the main window from the GUI and all data
    associated with it.
    """

    def __init__(self):
        """
        Builds the window. Connects all the signals and displays all the
        widgets.
        """
        super(MainWindow, self).__init__()
        self.set_size_request(800, 600)
        self.set_resizable(False)
        self.set_title(TITLE)
        self.set_icon_from_file(ROBOT_FILE)
        self.connect('delete_event', self.__on_exit)

        self._build_world()
        self._build_gui()
        self._paint_world()
        self.show()
        self.show_all()

    def _paint_world(self):
        """
        Paint the world known at this moment of time.
        """
        if self._world:
            self._world.fill(self._iworld)

        for i in xrange(N):
            for j in xrange(M):
                self._imgs[i][j].set_from_pixbuf(IMAGES[self._iworld[i][j]])

    def _build_world(self):
        """
        Builds the world in which the simulation takes place. Also, sets up
        several simulation variables (see below for each comment).
        """
        # Is the simulation in Play mode?
        self._running = False
        # Inhibit the last signal sent (used to disable a last callback after
        # Pause was clicked).
        self._inhibit = False
        # The world
        self._world = None
        self._iworld = []
        self._imgs = []
        for i in xrange(N):
            l = []
            limg = []
            for j in xrange(M):
                l.append(VOID)
                limg.append(gtk.Image())
            self._iworld.append(l)
            self._imgs.append(limg)

    def _build_gui(self):
        """
        Builds the interface of this window, the entire tree of widgets.
        """
        _vbox = gtk.VBox()
        self.add(_vbox)

        _toolbar = self._build_toolbar()
        _vbox.pack_start(_toolbar, False, False, 5)
        self._build_drawing_area(_vbox)
        self._plot_window = plot.Plot()
        self._plot_window.set_title(TITLE)
        self._plot_window.set_icon_from_file(ROBOT_FILE)

    def _build_drawing_area(self, _vbox):
        """
        Builds the drawing area: a table containing images for representing
        the maze.

        _vbox   parent containing the drawng area
        """
        _h = gtk.HBox()
        t = gtk.Table(N, M)
        for i in xrange(N):
            for j in xrange(M):
                t.attach(self._imgs[i][j], i, i+1, j, j+1)
        t.set_row_spacings(0)
        t.set_col_spacings(0)
        _h.pack_start(t, False, False, 10)
        _vbox.pack_start(_h, False, False, 5)

    def _build_toolbar(self):
        """
        Builds the toolbar and the associated buttons used to control the
        application.

        return  the Toolbar
        """
        _toolbar = gtk.Toolbar()
        _toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        _toolbar.set_style(gtk.TOOLBAR_BOTH)
        _toolbar.set_border_width(5)

        _btnNew = self._build_toolbar_button(gtk.STOCK_NEW, "New",
                "Starts a new simulation", self.__on_new_game)
        _toolbar.insert(_btnNew, -1)

        _toolbar.insert(gtk.SeparatorToolItem(), -1)
        self._build_simulation_buttons(_toolbar)
        _toolbar.insert(gtk.SeparatorToolItem(), -1)
        self._build_simulation_informations(_toolbar)
        _toolbar.insert(gtk.SeparatorToolItem(), -1)

        _btnAbout = self._build_toolbar_button(gtk.STOCK_ABOUT, "About",
                "About this program", self.__on_about)
        _toolbar.insert(_btnAbout, -1)

        self._switch_playstep_buttons(False)
        return _toolbar

    def _build_simulation_buttons(self, _toolbar):
        """
        Builds the buttons associated with the simulation: Play/Pause,
        Step,...

        _toolbar    The toolbar where to place the buttons.
        """
        self._btnStep = self._build_toolbar_button(gtk.STOCK_GO_FORWARD,
                "Step", "Do one step of the simulation", self.__on_step)
        _toolbar.insert(self._btnStep, -1)

        self._btnPlayPause = self._build_toolbar_button(gtk.STOCK_MEDIA_PLAY,
                "Play", "Play the simulation", self.__on_play)
        _toolbar.insert(self._btnPlayPause, -1)

        self._btnShowPlot = self._build_toolbar_button(gtk.STOCK_PAGE_SETUP,
                "Plot", "Show or hide plot of rewards", self.__on_plot)
        _toolbar.insert(self._btnShowPlot, -1)

        self._btnSavePlot = self._build_toolbar_button(gtk.STOCK_SAVE,
                "Save", "Save plot of simulation", self.__on_save)
        _toolbar.insert(self._btnSavePlot, -1)

    def _build_simulation_informations(self, _toolbar):
        """
        Builds the labels containing informations about the current epoch

        _toolbar    The toolbar where to place the buttons.
        """
        self._lblStep, ti = self._build_toolbar_label('Current step: ', '0')
        _toolbar.insert(ti, -1)
        _toolbar.insert(gtk.SeparatorToolItem(), -1)
        self._lblRew, ti = self._build_toolbar_label('Total reward: ', '0')
        _toolbar.insert(ti, -1)

    def _build_toolbar_button(self, img_stock, label, tooltip, callback):
        """
        Adds a new button to a toolbar.

        img_stock   stock image to use
        label       label of button
        tooltip     tooltip for the button
        callback    callback when button is clicked

        return      the button
        """
        img = gtk.Image()
        img.set_from_stock(img_stock, gtk.ICON_SIZE_LARGE_TOOLBAR)
        btn = gtk.ToolButton(img, label)
        btn.set_tooltip_text(tooltip)
        btn.connect('clicked', callback)
        return btn

    def _build_toolbar_label(self, info, label):
        """
        Adds a new label to a toolbar, used to display some information.

        info    text for the info label
        label   label to be created (text for it)

        return  the label and its container
        """
        ti = gtk.ToolItem()
        b = gtk.HBox()
        l = gtk.Label(info)
        b.pack_start(l, False, False, 5)
        lbl = gtk.Label(label)
        b.pack_start(lbl, False, False, 5)
        ti.add(b)
        return (lbl, ti)

    def _switch_play_button_type(self):
        """
        Used to switch the type of play/pause button.
        """
        if self._running:
            label = 'Pause'
            img_stock = gtk.STOCK_MEDIA_PAUSE
        else:
            label = 'Play'
            img_stock = gtk.STOCK_MEDIA_PLAY
        self._btnSavePlot.set_sensitive(label == 'Play')
        self._btnPlayPause.get_icon_widget().set_from_stock(img_stock,
                gtk.ICON_SIZE_LARGE_TOOLBAR)
        self._btnPlayPause.set_label(label)

    def _switch_playstep_buttons(self, state):
        """
        Used to enable or disable the animation buttons.

        state   sensitive status of the buttons (True if enabled)
        """
        self._btnStep.set_sensitive(state)
        self._btnPlayPause.set_sensitive(state)
        self._btnShowPlot.set_sensitive(state)
        self._btnSavePlot.set_sensitive(state)

    def __on_exit(self, widget, data=None):
        """
        Called when destroying the main window. Leave the gtk threads (and
        finish application).
        """
        gtk.main_quit()

    def __on_new_game(self, widget, data=None):
        """
        Called when the user issues a request for a new game.
        """
        if self._running:
            self._running = False
            self._inhibit = True
            self._switch_play_button_type()
        cfg = config.Config(self, TITLE)
        cfg.display()
        r = cfg.get_settings()
        cfg.destroy()
        self._switch_playstep_buttons(r != None)
        if r:
            self._world = world.World(r)
            self._plot_window.reset()
            self._paint_world()

    def __step(self):
        """
        Callback function used to generate one more step from the simulation.

        This is called exactly once by Step button's callback and as long as
        it is needed as a timer callback set from the Play button's callback.
        Because user might have pressed Pause before running this function, it
        has to check if the simulation is still running and return the valid
        response.

        Since the simulation never ends, the only time we return False is when
        the Pause button is pressed or a new simulation is started.

        return True if this functions should be called at a later time.
        """
        if self._inhibit:
            self._inhibit = False
            # do nothing, stop callbacks
            return False

        ret = self._world.step()
        self._plot_window.receive_reward(*ret)
        self._lblStep.set_text('{0}'.format(self._plot_window.get_step()))
        self._lblRew.set_text('{0}'.format(self._plot_window.get_rew()))
        self._paint_world()
        return self._running

    def __on_step(self, widget, data=None):
        """
        Called when the user clicks the Step button.
        """
        self.__step()

    def __on_play(self, widget, data=None):
        """
        Called when the user clicks the Play/Pause button.
        """
        self._running = not self._running
        self._switch_play_button_type()
        if self._running:
            self._btnStep.set_sensitive(False)
            glib.timeout_add(25, self.__step)
            self.__step()
        else:
            self._inhibit = True
            self._btnStep.set_sensitive(True)

    def __on_plot(self, widget, data=None):
        """
        Called when the user switches the status of the plot window.
        """
        self._plot_window.switch_state()

    def __on_save(self, widget, data=None):
        """
        Called when the user decides to save the plotted data.
        """
        self._plot_window.save_data()

    def __on_about(self, widget, data=None):
        """
        Called when the user issues a request for the About dialog.
        """
        aboutDialog = gtk.AboutDialog()
        aboutDialog.set_name(TITLE)
        aboutDialog.set_authors(["Mihai Maruseac <mihai.maruseac@rosedu.org>"])
        aboutDialog.set_documenters(
                ["Mihai Maruseac <mihai.maruseac@rosedu.org>"])
        aboutDialog.set_artists(
                ["Art taken from Public Domain pictures on the web"])
        aboutDialog.set_comments(
            "Simulate a robot trapped in a grid.\nThe robot must learn to stay "
            "within a certain corridor in the grid.\nSee README and LICENSE "
            "for more information.")
        aboutDialog.set_copyright(
            "Copyright © 2011 - 2012 Mihai Maruseac <mihai.maruseac@rosedu.org>")
        aboutDialog.set_logo(self.get_icon())
        aboutDialog.set_icon(self.get_icon())
        aboutDialog.set_version("0.1")
        aboutDialog.run()
        aboutDialog.destroy()

def main():
    """
    Main function. Construct the windows and start all application threads.
    """
    initImages()
    w = MainWindow()
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()

if __name__ == '__main__':
    main()

