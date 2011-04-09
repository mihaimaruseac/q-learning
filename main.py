#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import gtk
import glib

import config

TITLE = "Robot in a Grid"

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
        self.set_icon_from_file('robot.png')
        self.connect('delete_event', self.__on_exit)

        self._build_gui()
        self.show()
        self.show_all()

        # Is the simulation in Play mode?
        self._running = False
        # Inhibit the last signal sent (used to disable a last callback after
        # Pause was clicked).
        self._inhibit = False

        # No world is built now, it will be built after the config is
        # displayed.
        self._world = None

    def _build_gui(self):
        """
        Builds the interface of this window, the entire tree of widgets.
        """
        _vbox = gtk.VBox()
        self.add(_vbox)

        _toolbar = self._build_toolbar()
        _vbox.pack_start(_toolbar, False, False, 5)

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

        _btnAbout = self._build_toolbar_button(gtk.STOCK_ABOUT, "About",
                "About this program", self.__on_about)
        _toolbar.insert(_btnAbout, -1)

        self._btnStep.set_sensitive(False)
        self._btnPlayPause.set_sensitive(False)
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
#TODO: actual invocation
        print "Called"
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
            glib.timeout_add_seconds(1, self.__step)
            self.__step()
        else:
            self._inhibit = True
            self._btnStep.set_sensitive(True)

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
    w = MainWindow()
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()

if __name__ == '__main__':
    main()

