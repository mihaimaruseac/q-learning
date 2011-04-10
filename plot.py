#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

PLOTSIZE = 400
PAD = 10
R = 4

import gtk
import cPickle

class Plot(gtk.Window):
    """
    Contains the definitions for a window in which we plot a graphic of
    rewards across time.
    """

    def __init__(self):
        """
        Builds the window.
        """
        super(Plot, self).__init__()
        self.set_size_request(PLOTSIZE + 2 * PAD, PLOTSIZE + 2 * PAD)
        self.set_resizable(False)
        self.set_deletable(False)
        self._visible = False
        self._build_gui()
        self.reset()

    def switch_state(self):
        """
        Switches the visibility of this window.
        """
        self._visible = not self._visible
        if self._visible:
            self.present()
        else:
            self.hide()

    def receive_reward(self, end_of_epoch, reward):
        """
        Receives an reward and a flag indicating the an epoch was ended.
        """
        self._step += 1
        self._rewards[self._rcount] = reward
        if end_of_epoch:
            self._step = 0
            self._rcount += 1
            self._rewards.append(0)
        self._do_plot()

    def get_step(self):
        """
        Returns the current step in the current epoch.
        """
        return self._step

    def get_rew(self):
        """
        Returns the current total reward.
        """
        return self._rewards[self._rcount]

    def _do_plot(self):
        """
        Plots the rewards.
        """
        m = min([0, min(self._rewards)]) - PAD
        M = max([0, max(self._rewards)]) + PAD
        dy = (PLOTSIZE + 0.0) / (m - M)
        dx = (PLOTSIZE + 0.0) / (self._rcount + 2)
        corners = []
        for i in range(self._rcount + 1):
            corners.append((int(dx * (i + 1)), int(dy * (self._rewards[i] - M))))

        gc = self.get_style().white_gc
        self._pixmap.draw_rectangle(gc, True, 0, 0, PLOTSIZE, PLOTSIZE)

        gc = self.get_style().black_gc
        if len(corners) > 1:
            self._pixmap.draw_lines(gc, corners)

        gc.set_rgb_fg_color(gtk.gdk.Color(green=.8))
        for c in corners:
            self._pixmap.draw_arc(gc, True, c[0] - R, c[1] - R, 2 * R, 2 * R,
                    0, 360 * 64)

        gc.set_rgb_fg_color(gtk.gdk.Color(red=.8))
        x = int(dx * (self._rcount + 1))
        y = int(dy * (0 - M))
        self._pixmap.draw_arc(gc, True, x - R, y - R, 2 * R, 2 * R, 0, 360 * 64)

        gc.set_rgb_fg_color(gtk.gdk.Color(red=0))
        self._canvas.queue_draw_area(0, 0, PLOTSIZE, PLOTSIZE)

    def reset(self):
        """
        Resets internal data between simulations.
        """
        self._rewards = [0]
        self._rcount = 0
        self._step = 0
        self._do_plot()

    def save_data(self):
        """
        Called when plotted data should be saved. Because we are sure that all
        indices below self._rcount are static, we will save only those values.

        To do this very quickly, use pickle
        """
        btn = (gtk.STOCK_OK, gtk.RESPONSE_NONE,
                gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
        d = gtk.FileChooserDialog('Select filename to save to:', self,
                gtk.FILE_CHOOSER_ACTION_SAVE, btn)
        if d.run() == gtk.RESPONSE_NONE:
            filename = d.get_filename()
            with open(filename, "w") as f:
                cPickle.dump(self._rewards[:self._rcount], f)
        d.destroy()

    def _build_gui(self):
        """
        Builds the minimal GUI for this window.
        """
        fixed = gtk.Fixed()
        self.add(fixed)

        self._canvas = canvas = gtk.DrawingArea()
        canvas.set_size_request(PLOTSIZE, PLOTSIZE)
        canvas.connect('expose_event', self.__on_paint)
        fixed.put(canvas, PAD, PAD)

        self.show_all()
        self.hide()

        self._pixmap = gtk.gdk.Pixmap(self.get_window(), PLOTSIZE, PLOTSIZE)

    def __on_paint(self, widget, data=None):
        """
        Used to repaint a part of the window.
        """
        x, y, w, h = data.area
        widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
                self._pixmap, x, y, x, y, w, h)

