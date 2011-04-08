#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2010), mihai.maruseac@rosedu.org
#

import gtk

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
        self.set_title(TITLE)
        self.connect('destroy', self.__on_exit)
        self.show()
        self.show_all()

    def __on_exit(self, widget, data=None):
        """
        Called when destroying the main window. Leave the gtk threads (and
        finish application).
        """
        gtk.main_quit()

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

