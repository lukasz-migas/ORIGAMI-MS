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
import os
import webbrowser
from subprocess import Popen
from time import gmtime
from time import strftime

import config as config
import dialogs
import mainWindow as mainWindow
import wx
from data_handling import data_handling
from IDs import ID_helpCite
from IDs import ID_helpGitHub
from IDs import ID_helpHomepage
from IDs import ID_helpNewVersion


class ORIGAMIMS(object):
    def __init__(self, *args, **kwargs):

        self.__wx_app = wx.App(redirect=False)
        self.run = None
        self.view = None
        self.init(*args, **kwargs)

    def start(self):
        self.view.Show()
        self.__wx_app.MainLoop()

    def quit(self):
        self.__wx_app.ProcessIdle()
        self.__wx_app.ExitMainLoop()
        self.view.Destroy()
        return True

    def endSession(self):
        wx.CallAfter(self.quit, force=True)

    def init(self, *args, **kwargs):

        self.config = config.config()
        self.icons = config.IconContainer()

        self.view = mainWindow.MyFrame(self, config=self.config, icons=self.icons, title="ORIGAMI-MS")
        self.wrensCMD = None
        self.wrensRun = None
        self.wrensReset = None
        self.currentPath = ""
        self.wrensInput = {"polarity": None, "activationZone": None, "method": None, "command": None}
        # Set current working directory
        self.config.cwd = os.getcwd()
        self.logging = True

        self.config.startTime = strftime("%H-%M-%S_%d-%m-%Y", gmtime())
        self.__wx_app.SetTopWindow(self.view)
        self.__wx_app.SetAppName("ORIGAMI-MS")
        self.__wx_app.SetVendorName("Lukasz G Migas, University of Manchester")

        self.check_log_path()
        #         # Log all events to
        #         if self.logging:
        #             sys.stdin = self.view.panelPlots.log
        #             sys.stdout = self.view.panelPlots.log
        #             sys.stderr = self.view.panelPlots.log

        self.on_import_config_on_start(evt=None)

        self.data_handling = data_handling(self, self.view, self.config)

    def check_log_path(self):
        log_directory = os.path.join(self.config.cwd, "logs")
        if not os.path.exists(log_directory):
            print("Directory logs did not exist - created a new one in {}".format(log_directory))
            os.makedirs(log_directory)

        # Generate filename
        if self.config.loggingFile_path is None:
            file_path = "origami_{}.log".format(self.config.startTime)
            self.config.loggingFile_path = os.path.join(log_directory, file_path)

    def on_open_link(self, evt):
        """Open selected webpage."""

        # set link
        links = {ID_helpHomepage: "home", ID_helpGitHub: "github", ID_helpCite: "cite", ID_helpNewVersion: "newVersion"}

        link = self.config.links[links[evt.GetId()]]

        # open webpage
        try:
            webbrowser.open(link, autoraise=1)
        except BaseException:
            pass

    def on_calculate_parameters(self, evt):
        """
        This function is to be used to setup path to save origami parameters
        """

        if not self.config.iActivationMode == "User-defined":
            if self.data_handling.onCheckParameters() is False:
                print("Please fill in all necessary fields first!")
                return
            divisibleCheck = abs(self.config.iEndVoltage - self.config.iStartVoltage) / self.config.iStepVoltage
            divisibleCheck2 = divisibleCheck % 1
            if divisibleCheck2 != 0:
                msg = "Are you sure your collision voltage range is divisible by your increment?"
                dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
                return
        else:
            if self.config.iScanTime is None or self.config.iScanTime == "":
                msg = "Please make sure you to fill in the scan time input box."
                dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
                return

        if self.config.iActivationMode == "Linear":
            self.wrensInput, ColEnergyX, scanPerVoltageList, timeList, totalAcqTime = (
                self.data_handling.onPrepareLinearMethod()
            )
        elif self.config.iActivationMode == "Exponential":
            self.wrensInput, ColEnergyX, scanPerVoltageList, timeList, totalAcqTime = (
                self.data_handling.onPrepareExponentialMethod()
            )
        elif self.config.iActivationMode == "Boltzmann":
            self.wrensInput, ColEnergyX, scanPerVoltageList, timeList, totalAcqTime = (
                self.data_handling.onPrepareBoltzmannMethod()
            )
        elif self.config.iActivationMode == "User-defined":
            self.wrensInput, ColEnergyX, scanPerVoltageList, timeList, totalAcqTime = (
                self.data_handling.onPrepareListMethod()
            )

        self.wrensCMD = self.wrensInput.get("command", None)
        # Setup status:
        self.view.SetStatusText("".join(["Acq. time: ", str(totalAcqTime), " mins"]), number=0)
        self.view.SetStatusText("".join([str(len(scanPerVoltageList)), " steps"]), number=1)

        # Add wrensCMD to config file
        self.config.wrensCMD = self.wrensCMD

        self.on_plot_spv(ColEnergyX, scanPerVoltageList)
        self.on_plot_time(ColEnergyX, timeList)
        print("".join(["Your submission code: ", self.wrensCMD]))

    def on_start_wrens_runner(self, evt):

        if self.wrensCMD is None:
            msg = "Are you sure you filled in correct details or pressed calculate?"
            dialogs.dlgBox(
                exceptionTitle="Please complete all necessary fields and press Calculate",
                exceptionMsg=msg,
                type="Error",
            )
            return

        # A couple of checks to ensure the method in the settings is the one
        # currently available in memory..
        if self.wrensInput.get("polarity", None) != self.config.iPolarity:
            msg = "The polarity of the current method and the one in the window do not agree. Consider re-calculating."
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            return
        if self.wrensInput.get("activationZone", None) != self.config.iActivationZone:
            msg = "The activation zone of the current method and the one in the window do not agree. Consider re-calculating."
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            return
        if self.wrensInput.get("method", None) != self.config.iActivationMode:
            msg = "The acquisition mode of the current method and the one in the window do not agree. Consider re-calculating."
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            return
        if self.wrensInput.get("command", None) != self.wrensCMD:
            msg = "The command in the memory and the current method and the one in the window do not agree. Consider re-calculating."
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            return

        print("".join(["Your code: ", self.wrensCMD]))

        self.wrensRun = Popen(self.wrensCMD)

    def on_stop_wrens_runner(self, evt):

        if self.wrensRun:
            print("Stopped acquisition and reset the property banks")
            self.wrensRun.kill()
            self.wrensReset = Popen(self.config.wrensResetPath)
            self.view.panelControls.goBtn.Enable()
        else:
            print("You have to start acquisition first!")

    def on_fill_in_default_values(self, evt=None):
        """
        This function fills in default values in case you are being lazy!
        """
        pass

    def on_get_masslynx_path(self, evt):
        """
        Select path to the MassLynx folder
        """

        dlg = wx.DirDialog(self.view, "Select output directory...", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            print("You chose %s" % dlg.GetPath())
            self.view.panelControls.path_value.SetValue(dlg.GetPath())
            self.currentPath = dlg.GetPath()

    def on_import_config(self, evt):
        """
        This function imports configuration file
        """
        dlg = wx.FileDialog(
            self.view, "Open Configuration File", wildcard="*.ini", style=wx.FD_DEFAULT_STYLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            fileName = dlg.GetPath()
            self.config.importConfig(fileName=fileName, e=None)
            print("".join(["WREnS runner path: ", self.config.wrensRunnerPath]))
            print("".join(["Linear path: ", self.config.wrensLinearPath]))
            print("".join(["Exponent path: ", self.config.wrensExponentPath]))
            print("".join(["Boltzmann path: ", self.config.wrensBoltzmannPath]))
            print("".join(["List path: ", self.config.wrensUserDefinedPath]))
            print("".join(["Reset path: ", self.config.wrensResetPath]))

    def on_import_config_on_start(self, evt):
        print("Importing origamiConfig.ini")
        self.config.importConfig(fileName="origamiConfig.ini", e=None)

        print("".join(["WREnS runner path: ", self.config.wrensRunnerPath]))
        print("".join(["Linear path: ", self.config.wrensLinearPath]))
        print("".join(["Exponent path: ", self.config.wrensExponentPath]))
        print("".join(["Boltzmann path: ", self.config.wrensBoltzmannPath]))
        print("".join(["List path: ", self.config.wrensUserDefinedPath]))
        print("".join(["Reset path: ", self.config.wrensResetPath]))

    def onExportConfig(self, evt):
        """
        This function exports configuration file
        """
        dlg = wx.FileDialog(
            self.view, "Save As Configuration File", wildcard="*.ini", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        if dlg.ShowModal() == wx.ID_OK:
            fileName = dlg.GetPath()
            self.config.exportConfig(fileName=fileName, e=None)

    def on_save_parameters(self, evt):
        dlg = wx.FileDialog(
            self.view,
            "Save As ORIGAMI configuration File",
            wildcard="*.conf",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        )
        dlg.SetFilename("origami.conf")
        if dlg.ShowModal() == wx.ID_OK:
            fileName = dlg.GetPath()
            self.config.exportOrigamiConfig(fileName=fileName, e=None)

    def onLoadCSVList(self, evt):
        """
        This function loads a two column list with Collision voltage | number of scans
        """
        dlg = wx.FileDialog(
            self.view, "Choose a file:", wildcard="*.txt; *.csv", style=wx.FD_DEFAULT_STYLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            print("You chose %s" % dlg.GetPath())
            self.config.CSVFilePath = dlg.GetPath()

    def on_plot_spv(self, xvals, yvals):
        self.view.panelPlots.plot1.clearPlot()
        self.view.panelPlots.plot1.on_plot_1D(
            xvals=xvals, yvals=yvals, title="", xlabel="Collision Voltage (V)", ylabel="SPV"
        )
        # Show the mass spectrum
        self.view.panelPlots.plot1.repaint()

    def on_plot_time(self, xvals, yvals):
        self.view.panelPlots.plot2.clearPlot()
        self.view.panelPlots.plot2.on_plot_1D(
            xvals=xvals, yvals=yvals, title="", xlabel="Collision Voltage (V)", ylabel="Accumulated Time (s)"
        )
        # Show the mass spectrum
        self.view.panelPlots.plot2.repaint()


if __name__ == "__main__":
    app = ORIGAMIMS()
    app.start()
