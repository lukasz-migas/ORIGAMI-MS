# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
#    Copyright (C) 2017 Lukasz G. Migas <lukasz.migas@manchester.ac.uk>
#    This program is free software. Feel free to redistribute it and/or
#    modify it under the condition you cite and credit the authors whenever
#    appropriate.
#    The program is distributed in the hope that it will be useful but is
#    provided WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
# -------------------------------------------------------------------------
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
from ZoomBox import GetXValues
from ZoomBox import ZoomBox


class plottingWindow(wx.Window):
    def __init__(self, *args, **kwargs):

        if "figsize" in kwargs:
            self.figure = Figure(figsize=kwargs["figsize"])
            self._axes = [0.1, 0.1, 0.8, 0.8]
            del kwargs["figsize"]
        else:
            self.figure = Figure(figsize=[8, 2.5])

        self.figure.set_facecolor("white")

        wx.Window.__init__(self, *args, **kwargs)
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)
        self.figure.set_facecolor("white")
        self.figure.set_edgecolor("white")
        self.canvas.SetBackgroundColour("white")

        # Create a resizer
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.resize = 1

        #         self.canvas.mpl_connect('motion_notify_event', self.onMotion)

        # Prepare for zoom
        self.zoom = None
        self.zoomtype = "box"

    def setup_zoom(self, plots, zoom, data_lims=None):
        self.data_limits = data_lims
        self.zoom = ZoomBox(
            plots,
            None,
            drawtype="box",
            useblit=True,
            button=1,
            onmove_callback=None,
            rectprops=dict(alpha=0.2, facecolor="yellow"),
            spancoords="data",
            data_lims=data_lims,
        )

    def setupGetXAxies(self, plots):
        self.getxaxis = GetXValues(plots)

    def repaint(self):
        """
        Redraw and refresh the plot.
        :return: None
        """
        self.canvas.draw()

    def clearPlot(self, *args):
        """
        Clear the plot and rest some of the parameters.
        :param args: Arguments
        :return:
        """
        self.figure.clear()
        self.repaint()

    def on_resize(self, *args, **kwargs):
        if self.resize == 1:
            self.canvas.SetSize(self.GetSize())
