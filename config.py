# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import gtk

class Config(object):
    """
    Holds the definition for the configuration dialog showed before starting
    a new simulation.

    Simple workflow:
        __init__ -> display -> get_settings -> destroy
    """

    def __init__(self, parent, title=''):
        """
        Constructs the config dialog, always with the same initial values.

        parent  Parent window for the dialog
        title   Title for the dialog
        """
        btn = (gtk.STOCK_OK, gtk.RESPONSE_NONE,
                gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
        self._d = gtk.Dialog(title, parent,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, btn)
        self._d.set_deletable(False)
        self._d.set_size_request(400, 300)
        self._build_gui()
        self._d.show_all()

    def _build_gui(self):
        """
        Builds the entire GUI for this dialog.
        """
        self._topVBox = gtk.VBox()
        self._build_IO_gui()
        self._checkHBox = gtk.HBox()
        self._build_action_gui()
        self._build_learning_gui()
        self._topVBox.pack_start(self._checkHBox, False, False, 5)
        self._d.vbox.add(self._topVBox)

    def _build_IO_gui(self):
        """
        Builds the GUI for the UI actions: what file to read and whether to
        display plots while learning (in a new window).

        The plots comparing the two learning methods or any other comparisons
        will be done with a different tool, using the plots obtained via the
        above mentioned window, which should be saved to a file. See README
        for more.
        """
        self._fileHBox = gtk.HBox()
        self._fileLabel = gtk.Label('Input filename:')
        self._fileHBox.pack_start(self._fileLabel, False, False, 5)
        self._fileChoose = gtk.FileChooserButton("Select input filename")
        self._fileHBox.pack_start(self._fileChoose, True, True, 5)
        self._btnPlots = gtk.CheckButton("Draw plots")
        self._fileHBox.pack_start(self._btnPlots, False, False, 5)
        self._topVBox.pack_start(self._fileHBox, False, False, 5)

    def _build_action_gui(self):
        """
        Builds the action selection GUI. Basically, it should allow selecting
        between choosing action using e-greedy method or using softmax
        selection. In both cases, there is one parameter to select, tweaking
        the process.
        """
        self._frameActionSelection = gtk.Frame('Action Selection')
        self._asVBox = gtk.VBox()
        self._frameActionSelection.add(self._asVBox)
        self._checkHBox.pack_start(self._frameActionSelection, True, True, 5)

    def _build_learning_gui(self):
        """
        Builds the learning method selection GUI. Either Q-learning or SARSA
        is used. Also, it has to offer a way to select the two learning
        parameters.
        """
        self._frameLearningMethod = gtk.Frame('Learning Method')
        self._checkHBox.pack_start(self._frameLearningMethod, True, True, 5)

    def display(self):
        """
        Displays this dialog, letting the user to chose the options.
        """
        print self._d.run()

    def get_settings(self):
        """
        Returns the user's options. To be called only after hiding the dialog.
        """
        pass

    def destroy(self):
        """
        Destroys this window. Should be called after reading user options with
        the above function. After this call, any access to this instance can
        result in bugs.
        """
        self._d.destroy()

