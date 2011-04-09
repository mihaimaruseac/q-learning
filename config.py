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
        self._d.set_size_request(400, 220)
        self._build_gui()
        self._d.show_all()

        # holds the settings (uses to be a dictionary if everything is ok)
        self._configDict = None

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

        self._rLabel = gtk.Label('Max steps:')
        self._fileHBox.pack_start(self._rLabel, False, False, 5)
        self._rCounter = gtk.SpinButton(gtk.Adjustment(step_incr=100))
        self._rCounter.set_numeric(True)
        self._rCounter.set_wrap(True)
        self._rCounter.set_range(100, 10000)
        self._fileHBox.pack_start(self._rCounter, True, True, 5)

        self._topVBox.pack_start(self._fileHBox, False, False, 5)

    def _build_action_gui(self):
        """
        Builds the action selection GUI. Basically, it should allow selecting
        between choosing action using ε-greedy method or using softmax
        selection. In both cases, there is one parameter to select, tweaking
        the process (ε or τ).
        """
        self._frameActionSelection = gtk.Frame('Action Selection')
        self._checkHBox.pack_start(self._frameActionSelection, True, True, 5)

        self._asVBox = gtk.VBox()
        self._frameActionSelection.add(self._asVBox)

        self._greedyAction = gtk.RadioButton(None, 'Use ε-greedy selection')
        self._greedyAction.connect('clicked', self.__on_greedy)
        self._asVBox.add(self._greedyAction)

        self._eHBox = gtk.HBox()
        self._eLabel = gtk.Label('ε value:')
        self._eHBox.pack_start(self._eLabel, False, False, 5)
        self._eCounter = gtk.SpinButton(gtk.Adjustment(step_incr=.05), digits=2)
        self._eCounter.set_numeric(True)
        self._eCounter.set_wrap(True)
        self._eCounter.set_range(.1, .9)
        self._eHBox.pack_start(self._eCounter, True, True, 5)
        self._asVBox.add(self._eHBox)

        self._softmaxAction = gtk.RadioButton(self._greedyAction,
                'Use softmax selection')
        self._softmaxAction.connect('clicked', self.__on_softmax)
        self._asVBox.add(self._softmaxAction)

        self._tHBox = gtk.HBox()
        self._tLabel = gtk.Label('τ value:')
        self._tHBox.pack_start(self._tLabel, False, False, 5)
        self._tCounter = gtk.SpinButton(gtk.Adjustment(step_incr=.1), digits=1)
        self._tCounter.set_numeric(True)
        self._tCounter.set_wrap(True)
        self._tCounter.set_range(1, 10)
        self._tCounter.set_sensitive(False)
        self._tHBox.pack_start(self._tCounter, True, True, 5)
        self._asVBox.add(self._tHBox)

    def _build_learning_gui(self):
        """
        Builds the learning method selection GUI. Either Q-learning or SARSA
        is used. Also, it has to offer a way to select the two learning
        parameters (α and γ).
        """
        self._frameLearningMethod = gtk.Frame('Learning Method')
        self._checkHBox.pack_start(self._frameLearningMethod, True, True, 5)

        self._lmVBox = gtk.VBox()
        self._frameLearningMethod.add(self._lmVBox)

        self._ql = gtk.RadioButton(None, 'Use Q-learning')
        self._lmVBox.add(self._ql)

        self._sarsa = gtk.RadioButton(self._ql, 'Use SARSA')
        self._lmVBox.add(self._sarsa)

        self._aHBox = gtk.HBox()
        self._aLabel = gtk.Label('α value:')
        self._aHBox.pack_start(self._aLabel, False, False, 5)
        self._aCounter = gtk.SpinButton(gtk.Adjustment(step_incr=.05), digits=2)
        self._aCounter.set_numeric(True)
        self._aCounter.set_wrap(True)
        self._aCounter.set_range(0, 1)
        self._aHBox.pack_start(self._aCounter, True, True, 5)
        self._lmVBox.add(self._aHBox)

        self._gHBox = gtk.HBox()
        self._gLabel = gtk.Label('γ value:')
        self._gHBox.pack_start(self._gLabel, False, False, 5)
        self._gCounter = gtk.SpinButton(gtk.Adjustment(step_incr=.05), digits=2)
        self._gCounter.set_numeric(True)
        self._gCounter.set_wrap(True)
        self._gCounter.set_range(0, 1)
        self._gHBox.pack_start(self._gCounter, True, True, 5)
        self._lmVBox.add(self._gHBox)

    def display(self):
        """
        Displays this dialog, letting the user to chose the options. After the
        dialog is closed, check the user inputs and construct the settings
        dictionary.
        """
        if self._d.run() == gtk.RESPONSE_REJECT:
            self._configDict = None # nothing to return
            return None
        self._configDict = {}

        # Try to read the file provided
        if not self._read(self._fileChoose.get_filename()):
            md = gtk.MessageDialog(self._d, gtk.DIALOG_DESTROY_WITH_PARENT,
                    gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Invalid file!")
            md.run()
            md.destroy()
            # Try again, hopefully we won't recourse too many times.
            self.display()

        # If everything is ok here, read info from the other widgets,
        # complete the dictionary and return (the other widgets always
        # return good values).
        self._complete_config()

    def get_settings(self):
        """
        Returns the user's options. To be called only after hiding the dialog.
        Simply returns the dictionary.
        """
        d = self._configDict
        self._configDict = None
        return d

    def destroy(self):
        """
        Destroys this window. Should be called after reading user options with
        the above function. After this call, any access to this instance can
        result in bugs.
        """
        self._d.destroy()

    def _read(self, fName):
        """
        Reads the user provided filename to obtain information about the
        simulation. Completes the _configDict.

        return  True if everything is ok
        """
        if not fName:
            return False

        try:
            with open(fName) as f:
                d = f.readline()
                p = d.split()
                if len(p) != 2:
                    return False
                self._configDict['N'] = int(p[0])
                self._configDict['M'] = int(p[1])
                d = f.readline()
                self._configDict['D'] = int(d)
                d = f.readline()
                p = d.split()
                if len(p) != 2:
                    return False
                self._configDict['xs'] = int(p[0])
                self._configDict['ys'] = int(p[1])
                d = f.readline()
                self._configDict['d1'] = int(d)
                d = f.readline()
                self._configDict['d2'] = int(d)
        except Exception as e:
            return False
        return True

    def _complete_config(self):
        """
        Reads data from the dialog's widgets to complete the _configDict.
        """
        self._configDict['greedy?'] = b = self._greedyAction.get_active()
        if b:
            self._configDict['ε/τ'] = self._eCounter.get_value()
        else:
            self._configDict['ε/τ'] = self._tCounter.get_value()
        self._configDict['Q?'] = self._ql.get_active()
        self._configDict['α'] = self._aCounter.get_value()
        self._configDict['γ'] = self._gCounter.get_value()
        self._configDict['runs'] = self._rCounter.get_value()

    def __on_greedy(self, widget, data=None):
        """
        Called when the user clicks the greedy action selection button.
        """
        self._eCounter.set_sensitive(True)
        self._tCounter.set_sensitive(False)

    def __on_softmax(self, widget, data=None):
        """
        Called when the user clicks the greedy action selection button.
        """
        self._eCounter.set_sensitive(False)
        self._tCounter.set_sensitive(True)

