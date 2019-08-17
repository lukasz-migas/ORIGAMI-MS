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
import logging
from time import gmtime
from time import strftime

import matplotlib
import numpy as np
import wx
from origamiStyles import makeMenuItem
from plottingWindow import plottingWindow

logger = logging.getLogger("origami")


class panelPlot(wx.Panel):
    def __init__(self, parent, config):
        wx.Panel.__init__(
            self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(350, 600), style=wx.TAB_TRAVERSAL
        )

        self.parent = parent
        self.config = config
        self.page_name = None
        self.startTime = strftime("%H-%M-%S_%d-%m-%Y", gmtime())
        self.config.startTime = self.startTime

        self.make_notebook()

    def make_notebook(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        # Setup notebook
        self.plotNotebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Setup PLOT SPV
        self.panelSPV = wx.Panel(self.plotNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.plotNotebook.AddPage(self.panelSPV, "Scans per Voltage", False)

        self.plot1 = plot_1D(self.panelSPV)
        box1 = wx.BoxSizer(wx.VERTICAL)
        box1.Add(self.plot1, 1, wx.EXPAND)
        self.panelSPV.SetSizer(box1)

        self.panelTime = wx.Panel(self.plotNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.plotNotebook.AddPage(self.panelTime, "Acquisition time", False)

        self.plot2 = plot_1D(self.panelTime)
        box2 = wx.BoxSizer(wx.VERTICAL)
        box2.Add(self.plot2, 1, wx.EXPAND)
        self.panelTime.SetSizer(box2)

        self.panelCVs = wx.Panel(self.plotNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.plotNotebook.AddPage(self.panelCVs, "Collision voltage steps", False)

        self.plot3 = plot_1D(self.panelCVs)
        box3 = wx.BoxSizer(wx.VERTICAL)
        box3.Add(self.plot3, 1, wx.EXPAND)
        self.panelCVs.SetSizer(box3)

        mainSizer.Add(self.plotNotebook, 1, wx.EXPAND | wx.ALL, 1)

        self.SetSize(0, 0, 420, 500)
        self.SetSizer(mainSizer)
        self.Layout()
        self.Show(True)

        self.Bind(wx.EVT_CONTEXT_MENU, self.on_right_click)

    def on_right_click(self, evt):

        menu = wx.Menu()
        menu_action_copy_to_clipboard = makeMenuItem(parent=menu, id=wx.ID_ANY, text="Copy plot to clipboard")
        menu.AppendItem(menu_action_copy_to_clipboard)

        self.Bind(wx.EVT_MENU, self.on_copy_to_clipboard, menu_action_copy_to_clipboard)

        self.PopupMenu(menu)
        menu.Destroy()
        self.SetFocus()

    def on_get_current_page(self):
        self.page_name = self.plotNotebook.GetPageText(self.plotNotebook.GetSelection())

    def on_plot_spv(self, xvals, yvals):
        self.plot1.clearPlot()
        self.plot1.on_plot_1D(xvals, yvals, title="", xlabel="Collision Voltage (V)", ylabel="SPV")
        self.plot1.repaint()

    def on_plot_time(self, xvals, yvals):
        self.plot2.clearPlot()
        self.plot2.on_plot_1D(xvals, yvals, title="", xlabel="Collision Voltage (V)", ylabel="Accumulated Time (s)")
        self.plot2.repaint()

    def on_plot_collision_voltages(self, xvals, yvals):
        self.plot3.clearPlot()
        self.plot3.on_plot_1D(xvals, yvals, title="", xlabel="Scans", ylabel="Collision Voltage (V)")
        self.plot3.repaint()

    def on_copy_to_clipboard(self, evt):
        self.on_get_current_page()
        plot_obj = self.get_plot_from_name(self.page_name)
        plot_obj.copy_to_clipboard()

    def get_plot_from_name(self, plot_name):
        plot_dict = {
            "Scans per Voltage": self.plot1,
            "Acquisition time": self.plot2,
            "Collision voltage steps": self.plot3,
        }

        return plot_dict.get(plot_name, None)


class plot_1D(plottingWindow):
    def __init__(self, *args, **kwargs):
        plottingWindow.__init__(self, *args, **kwargs)
        self.plotflag = False

    def on_plot_1D(self, xvals, yvals, xlabel, ylabel, title, zoom="box", axesSize=None, fontsize=10):

        self.plotflag = True  # Used only if saving data
        self.zoomtype = zoom
        if axesSize is None:
            self._axes = [0.15, 0.2, 0.8, 0.7]
        else:
            self._axes = axesSize
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.figure.set_facecolor("white")
        self.figure.set_edgecolor("white")
        self.canvas.SetBackgroundColour("white")
        matplotlib.rc("xtick", labelsize=fontsize)
        matplotlib.rc("ytick", labelsize=fontsize)

        self.plotSPV = self.figure.add_axes(self._axes)
        self.plotSPV.plot(xvals, yvals, color="black")

        xlimits = (np.min(xvals) - 1, np.max(xvals) + 1)
        ylimits = (np.min(yvals) * 0.9, np.max(yvals) * 1.1)

        self.plotSPV.set_xlim(xlimits)
        self.plotSPV.set_ylim(ylimits)

        self.plotSPV.set_xlabel(self.xlabel, fontsize=fontsize, weight="normal")
        self.plotSPV.set_ylabel(self.ylabel, fontsize=fontsize, weight="normal")

        extent = [xlimits[0], ylimits[0], xlimits[1], ylimits[1]]

        self.setup_zoom([self.plotSPV], self.zoomtype, data_lims=extent)

    def copy_to_clipboard(self):
        self.canvas.Copy_to_Clipboard()
        logger.info("Figure was copied to the clipboard")
