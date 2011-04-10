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
        self._d.set_size_request(420, 220)
        self._d.set_resizable(False)
        self._build_gui()
        self._d.show_all()

        # holds the settings (uses to be a dictionary if everything is ok)
        self._configDict = None

    def _build_gui(self):
        """
        Builds the entire GUI for this dialog.
        """
        _topVBox = gtk.VBox()
        self._build_IO_gui(_topVBox)
        _checkHBox = gtk.HBox()
        self._build_action_gui(_checkHBox)
        self._build_learning_gui(_checkHBox)
        _topVBox.pack_start(_checkHBox, False, False, 5)
        self._d.vbox.add(_topVBox)

    def _build_IO_gui(self, _topVBox):
        """
        Builds the GUI for the UI actions: what file to read and how many
        steps to take on each learning iteration.

        _topVBox    VBox holding the widgets built by this function
        """
        _fileHBox = gtk.HBox()
        _topVBox.pack_start(_fileHBox, False, False, 5)
        _fileLabel = gtk.Label('Input filename:')
        _fileHBox.pack_start(_fileLabel, False, False, 5)
        self._fileChoose = gtk.FileChooserButton("Select input filename")
        _fileHBox.pack_start(self._fileChoose, True, True, 5)
        self._rCounter = self._build_counter('Max steps:', 100, 10000, _fileHBox, 100, 0)

    def _build_action_gui(self, _checkHBox):
        """
        Builds the action selection GUI. Basically, it should allow selecting
        between choosing action using ε-greedy method or using softmax
        selection. In both cases, there is one parameter to select, tweaking
        the process (ε or τ).

        _checkHBox    HBox holding the widgets built by this function
        """
        _frameActionSelection = gtk.Frame('Action Selection')
        _checkHBox.pack_start(_frameActionSelection, True, True, 5)
        _asVBox = gtk.VBox()
        _frameActionSelection.add(_asVBox)

        self._greedyAction = gtk.RadioButton(None, 'Use ε-greedy selection')
        self._greedyAction.connect('clicked', self.__on_greedy)
        _asVBox.add(self._greedyAction)
        self._eCounter = self._build_counter('ε value:', .1, .9, _asVBox)

        _softmaxAction = gtk.RadioButton(self._greedyAction, 'Use softmax selection')
        _softmaxAction.connect('clicked', self.__on_softmax)
        _asVBox.add(_softmaxAction)
        self._tCounter = self._build_counter('τ value:', 1, 10, _asVBox, .1, 1, False)

    def _build_learning_gui(self, _checkHBox):
        """
        Builds the learning method selection GUI. Either Q-learning or SARSA
        is used. Also, it has to offer a way to select the two learning
        parameters (α and γ).

        _checkHBox    HBox holding the widgets built by this function
        """
        _frameLearningMethod = gtk.Frame('Learning Method')
        _checkHBox.pack_start(_frameLearningMethod, True, True, 5)
        _lmVBox = gtk.VBox()
        _frameLearningMethod.add(_lmVBox)

        self._ql = gtk.RadioButton(None, 'Use Q-learning')
        _lmVBox.add(self._ql)
        _sarsa = gtk.RadioButton(self._ql, 'Use SARSA')
        _lmVBox.add(_sarsa)

        self._aCounter = self._build_counter('α value:', 0.1, 1, _lmVBox)
        self._gCounter = self._build_counter('γ value:', 0.1, 1, _lmVBox)

    def _build_counter(self, text, minv, maxv, parent, incr=.05, digits=2, enabled=True):
        """
        Builds a SpinButton used to represent a fixed value in a fixed
        interval (for values of parameters).

        text        text explaining what the value stands for
        minv        minimal value for the counter
        maxv        maximal value for the counter
        parent      parent box for this counter
        incr        increment value for the spin button
        digits      decimal places to show in the button
        enabled     is the SpinButton available when it is built?
        return      the SpinButton built
        """
        _hBox = gtk.HBox()
        _label = gtk.Label(text)
        _hBox.pack_start(_label, False, False, 5)
        sb = gtk.SpinButton(gtk.Adjustment(step_incr=incr), digits=digits)
        sb.set_numeric(True)
        sb.set_wrap(True)
        sb.set_range(minv, maxv)
        sb.set_sensitive(enabled)
        _hBox.pack_start(sb, True, True, 5)
        parent.add(_hBox)
        return sb

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
            return self.display()

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

