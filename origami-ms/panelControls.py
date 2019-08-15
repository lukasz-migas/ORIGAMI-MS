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
from origamiStyles import makeStaticBox
from origamiStyles import makeStaticText
from origamiStyles import TEXT_STYLE_CV_R_L
from origamiStyles import TXTBOX_SIZE
from origamiStyles import validator
from utils.converters import str2int
from utils.converters import str2num


class panelControls(wx.Panel):
    def __init__(self, parent, presenter, config):
        wx.Panel.__init__(
            self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600, 400), style=wx.TAB_TRAVERSAL
        )

        self.parent = parent
        self.presenter = presenter
        self.config = config

        self.make_panel()
        self.on_toggle_controls(evt=None)

    def make_panel(self):

        # Main sizer for the panel
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Prepare notebooks
        self.settingsBook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        self.settingsBook_pane1 = wx.Panel(
            self.settingsBook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )
        self.settingsBook.AddPage(self.settingsBook_pane1, "Activation", False)
        self.make_origami_page()
        mainSizer.Add(self.settingsBook, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSize(420, 295)
        self.SetSizer(mainSizer)
        self.Layout()

    def make_origami_page(self):

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Gather sizers
        self.make_polarity_box()
        self.make_region_box()
        self.make_activation_box()
        origamiParams = self.make_origami_parameters_box()
        buttons = self.make_buttons_box()

        main_grid = wx.GridBagSizer(0, 0)
        main_grid.Add(self.polarityBox, (0, 0), wx.GBSpan(1, 2), flag=wx.EXPAND)
        main_grid.Add(self.activationZone, (1, 0), wx.GBSpan(1, 2), flag=wx.EXPAND)
        main_grid.Add(self.activationType, (2, 0), wx.GBSpan(2, 2), flag=wx.EXPAND)
        main_grid.Add(origamiParams, (0, 2), wx.GBSpan(4, 2), flag=wx.EXPAND)
        main_grid.Add(buttons, (4, 0), wx.GBSpan(2, 3))

        mainSizer.Add(main_grid, wx.EXPAND | wx.ALL, 0)

        self.settingsBook_pane1.SetSizer(mainSizer)
        self.settingsBook_pane1.Layout()

        # Make bindings
        self.polarityBox.Bind(wx.EVT_RADIOBOX, self.on_apply)
        self.activationZone.Bind(wx.EVT_RADIOBOX, self.on_apply)
        self.activationType.Bind(wx.EVT_RADIOBOX, self.on_apply)
        self.spv_input.Bind(wx.EVT_TEXT, self.on_apply)
        self.scanTime_input.Bind(wx.EVT_TEXT, self.on_apply)
        self.startVoltage_input.Bind(wx.EVT_TEXT, self.on_apply)
        self.endVoltage_input.Bind(wx.EVT_TEXT, self.on_apply)
        self.stepVoltage_input.Bind(wx.EVT_TEXT, self.on_apply)
        self.exponentialPerct_input.Bind(wx.EVT_TEXT, self.on_apply)
        self.exponentialIncrm_input.Bind(wx.EVT_TEXT, self.on_apply)
        self.boltzmann_input.Bind(wx.EVT_TEXT, self.on_apply)

        self.loadCSVBtn.Bind(wx.EVT_BUTTON, self.presenter.onLoadCSVList)

    def make_polarity_box(self):

        self.polarityBox = wx.RadioBox(
            self.settingsBook_pane1,
            wx.ID_ANY,
            "Ion polarity",
            choices=["Positive        ", "Negative        "],
            majorDimension=0,
            style=wx.RA_SPECIFY_COLS,
            size=(200, -1),
        )
        self.polarityBox.SetSelection(0)

    def make_region_box(self):

        self.activationZone = wx.RadioBox(
            self.settingsBook_pane1,
            wx.ID_ANY,
            "Activation region",
            choices=["Cone              ", "Trap             "],
            majorDimension=0,
            style=wx.RA_SPECIFY_COLS,
            size=(200, -1),
        )
        self.activationZone.SetSelection(1)

    def make_activation_box(self):

        self.activationType = wx.RadioBox(
            self.settingsBook_pane1,
            wx.ID_ANY,
            "Activation method",
            choices=["Linear", "Exponential", "Boltzmann", "User-defined"],
            majorDimension=2,
            style=wx.RA_SPECIFY_COLS,
            size=(200, -1),
        )
        self.activationType.SetSelection(0)

    def make_origami_parameters_box(self):

        origamiBox = makeStaticBox(self.settingsBook_pane1, "ORIGAMI parameters", (330, -1), wx.BLUE)

        origamiMainSizer = wx.StaticBoxSizer(origamiBox, wx.HORIZONTAL)

        spv_label = makeStaticText(self.settingsBook_pane1, "Scans per Voltage")
        self.spv_input = wx.TextCtrl(
            self.settingsBook_pane1, -1, "", size=(TXTBOX_SIZE, -1), validator=validator("intPos")
        )
        info_msg = "Scans per voltage - number of scans per voltage for each collision voltage. Value type: Integer"
        self.spv_input.SetToolTip(wx.ToolTip(info_msg))

        scanTime_label = makeStaticText(self.settingsBook_pane1, "Scan time (s)")
        self.scanTime_input = wx.TextCtrl(
            self.settingsBook_pane1, -1, "", size=(TXTBOX_SIZE, -1), validator=validator("floatPos")
        )
        info_msg = (
            "Scan time - length of each scan. Has to be the same as in MassLynx acquisition window!"
            + " Value type: Float. Range: 0.1-5"
        )
        self.scanTime_input.SetToolTip(wx.ToolTip(info_msg))

        startVoltage_label = makeStaticText(self.settingsBook_pane1, "Start voltage (V)")
        self.startVoltage_input = wx.TextCtrl(
            self.settingsBook_pane1, -1, "", size=(TXTBOX_SIZE, -1), validator=validator("floatPos")
        )
        info_msg = "Start voltage - starting value in the collision voltage ramp. Value type: Float. Range: 0-200"
        self.startVoltage_input.SetToolTip(wx.ToolTip(info_msg))

        endVoltage_label = makeStaticText(self.settingsBook_pane1, "End voltage (V)")
        self.endVoltage_input = wx.TextCtrl(
            self.settingsBook_pane1, -1, "", size=(TXTBOX_SIZE, -1), validator=validator("floatPos")
        )
        info_msg = "End voltage - final value in the collision voltage ramp. Value type: Float. Range: 0-200"
        self.endVoltage_input.SetToolTip(wx.ToolTip(info_msg))

        stepVoltage_label = makeStaticText(self.settingsBook_pane1, "Step voltage (V)")
        self.stepVoltage_input = wx.TextCtrl(
            self.settingsBook_pane1, -1, "", size=(TXTBOX_SIZE, -1), validator=validator("floatPos")
        )
        info_msg = "Step voltage - size of increment between each step. Value type: Float."
        self.stepVoltage_input.SetToolTip(wx.ToolTip(info_msg))

        exponentialPerct_label = makeStaticText(self.settingsBook_pane1, "Exponential (%)")
        self.exponentialPerct_input = wx.TextCtrl(
            self.settingsBook_pane1, -1, "", size=(TXTBOX_SIZE, -1), validator=validator("floatPos")
        )
        info_msg = (
            "Exponential percentage value - determines at which stage of collision voltage ramp the increase"
            + " in SPV should start. Value type: Float. Range: 0-100"
        )
        self.exponentialPerct_input.SetToolTip(wx.ToolTip(info_msg))

        exponentialIncrm_label = makeStaticText(self.settingsBook_pane1, "Exponential increment")
        self.exponentialIncrm_input = wx.TextCtrl(
            self.settingsBook_pane1, -1, "", size=(TXTBOX_SIZE, -1), validator=validator("floatPos")
        )
        info_msg = (
            "Exponential increment value - determines how rapidly the value of SPV increases."
            + " Value type: Float. Range: 0.01-0.075"
        )
        self.exponentialIncrm_input.SetToolTip(wx.ToolTip(info_msg))

        boltzmann_label = makeStaticText(self.settingsBook_pane1, "Boltzmann offset")
        self.boltzmann_input = wx.TextCtrl(
            self.settingsBook_pane1, -1, "", size=(TXTBOX_SIZE, -1), validator=validator("floatPos")
        )
        info_msg = (
            "Boltzmann offset value - determines how rapidly the value of SPV increases. Value type: Float."
            + " Range: 10-100"
        )
        self.boltzmann_input.SetToolTip(wx.ToolTip(info_msg))

        userDefined_label = makeStaticText(self.settingsBook_pane1, "User-defined")
        self.loadCSVBtn = wx.Button(self.settingsBook_pane1, -1, "Load list", size=(60, -1))
        info_msg = (
            "Load a .csv list SPVs and CVs. The file has to have a header with SPV and CV"
            + " labels and be comma-delimited."
        )
        self.loadCSVBtn.SetToolTip(wx.ToolTip(info_msg))

        grid = wx.GridBagSizer(2, 2)

        grid.Add(spv_label, wx.GBPosition(0, 0), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)
        grid.Add(self.spv_input, wx.GBPosition(0, 1), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)

        grid.Add(scanTime_label, wx.GBPosition(1, 0), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)
        grid.Add(self.scanTime_input, wx.GBPosition(1, 1), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)

        grid.Add(startVoltage_label, wx.GBPosition(2, 0), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)
        grid.Add(self.startVoltage_input, wx.GBPosition(2, 1), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)

        grid.Add(endVoltage_label, wx.GBPosition(3, 0), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)
        grid.Add(self.endVoltage_input, wx.GBPosition(3, 1), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)

        grid.Add(stepVoltage_label, wx.GBPosition(4, 0), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)
        grid.Add(self.stepVoltage_input, wx.GBPosition(4, 1), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)

        grid.Add(exponentialPerct_label, wx.GBPosition(0, 2), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)
        grid.Add(self.exponentialPerct_input, wx.GBPosition(0, 3), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)

        grid.Add(exponentialIncrm_label, wx.GBPosition(1, 2), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)
        grid.Add(self.exponentialIncrm_input, wx.GBPosition(1, 3), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)

        grid.Add(boltzmann_label, wx.GBPosition(2, 2), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)
        grid.Add(self.boltzmann_input, wx.GBPosition(2, 3), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)

        grid.Add(userDefined_label, wx.GBPosition(3, 2), wx.GBSpan(1, 1), TEXT_STYLE_CV_R_L, 2)
        grid.Add(self.loadCSVBtn, (3, 3), flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL)

        origamiMainSizer.Add(grid, 0, wx.EXPAND | wx.ALL, 2)

        return origamiMainSizer

    def make_buttons_box(self):
        mainSizer = wx.StaticBoxSizer(wx.StaticBox(self.settingsBook_pane1, -1, "", size=(552, -1)), wx.VERTICAL)

        self.pathBtn = wx.Button(self.settingsBook_pane1, -1, "Set path", size=(80, -1))
        info_msg = "Set path to MassLynx folder where acquisition takes place"
        self.pathBtn.SetToolTip(wx.ToolTip(info_msg))

        self.calculateBtn = wx.Button(self.settingsBook_pane1, -1, "Calculate", size=(80, -1))
        info_msg = "Calculate ORIGAMI parameters and pre-set WREnS command"
        self.calculateBtn.SetToolTip(wx.ToolTip(info_msg))

        self.saveParametersBtn = wx.Button(self.settingsBook_pane1, -1, "Save parameters", size=(100, -1))
        info_msg = (
            "Save ORIGAMI-MS parameters so ORIGAMI-ANALYSE can automatically" + " read them when viewing MassLynx file"
        )
        self.saveParametersBtn.SetToolTip(wx.ToolTip(info_msg))

        self.goBtn = wx.Button(self.settingsBook_pane1, -1, "Go", size=(80, -1))
        info_msg = "Start ORIGAMI-MS acquisition - Make sure you start acquisition in MassLynx first!"
        self.goBtn.SetToolTip(wx.ToolTip(info_msg))

        self.stopBtn = wx.Button(self.settingsBook_pane1, -1, "Stop", size=(80, -1))
        info_msg = "Stop ORIGAMI-MS acquisition - sends a 'kill' signal to stop WREnS script"
        self.stopBtn.SetToolTip(wx.ToolTip(info_msg))

        path_label = makeStaticText(self.settingsBook_pane1, "Path:")
        self.path_value = wx.TextCtrl(self.settingsBook_pane1, -1, "", size=(-1, -1))
        self.path_value.SetEditable(False)

        grid = wx.GridBagSizer(5, 5)
        grid.Add(self.pathBtn, (0, 1), flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        grid.Add(self.calculateBtn, (0, 2), flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        grid.Add(self.saveParametersBtn, (0, 3), flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        grid.Add(self.goBtn, (0, 4), flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        grid.Add(self.stopBtn, (0, 5), flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)

        grid.Add(path_label, (1, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(
            self.path_value,
            (1, 1),
            (1, 5),
            flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
        )

        # make bindings
        self.pathBtn.Bind(wx.EVT_BUTTON, self.presenter.on_get_masslynx_path)
        self.calculateBtn.Bind(wx.EVT_BUTTON, self.presenter.on_calculate_parameters)
        self.goBtn.Bind(wx.EVT_BUTTON, self.presenter.on_start_wrens_runner)
        self.stopBtn.Bind(wx.EVT_BUTTON, self.presenter.on_stop_wrens_runner)

        self.saveParametersBtn.Bind(wx.EVT_BUTTON, self.presenter.on_save_parameters)

        mainSizer.Add(grid, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        return mainSizer

    def on_apply(self, evt):

        polarityID = self.polarityBox.GetStringSelection()
        if polarityID == "Positive":
            self.config.iPolarity = "POSITIVE"
        else:
            self.config.iPolarity = "NEGATIVE"

        activationID = self.activationZone.GetStringSelection()
        if activationID == "Cone":
            self.config.iActivationZone = "CONE"
        else:
            self.config.iActivationZone = "TRAP"

        self.config.iActivationMode = self.activationType.GetStringSelection()

        self.config.iSPV = str2int(self.spv_input.GetValue())
        self.config.iScanTime = str2int(self.scanTime_input.GetValue())
        self.config.iStartVoltage = str2num(self.startVoltage_input.GetValue())
        self.config.iEndVoltage = str2num(self.endVoltage_input.GetValue())
        self.config.iStepVoltage = str2num(self.stepVoltage_input.GetValue())
        self.config.iExponentPerct = str2num(self.exponentialPerct_input.GetValue())
        self.config.iExponentIncre = str2num(self.exponentialIncrm_input.GetValue())
        self.config.iBoltzmann = str2num(self.boltzmann_input.GetValue())

        self.on_toggle_controls(evt=None)

    def importFromConfig(self, evt):

        self.spv_input.SetValue(str(self.config.iSPV))
        self.scanTime_input.SetValue(str(self.config.iScanTime))
        self.startVoltage_input.SetValue(str(self.config.iStartVoltage))
        self.endVoltage_input.SetValue(str(self.config.iEndVoltage))
        self.stepVoltage_input.SetValue(str(self.config.iStepVoltage))
        self.exponentialPerct_input.SetValue(str(self.config.iExponentPerct))
        self.exponentialIncrm_input.SetValue(str(self.config.iExponentIncre))
        self.boltzmann_input.SetValue(str(self.config.iBoltzmann))

        if self.config.iPolarity == "POSITIVE":
            self.polarityBox.SetSelection(0)
        elif self.config.iPolarity == "NEGATIVE":
            self.polarityBox.SetSelection(1)

        if self.config.iActivationZone == "Cone":
            self.activationZone.SetSelection(0)
        elif self.config.iActivationZone == "Trap":
            self.activationZone.SetSelection(1)

        if self.config.iActivationMode == "Linear":
            self.activationType.SetSelection(0)
        elif self.config.iActivationMode == "Exponential":
            self.activationType.SetSelection(1)
        elif self.config.iActivationMode == "Boltzmann":
            self.activationType.SetSelection(2)
        elif self.config.iActivationMode == "User-defined":
            self.activationType.SetSelection(3)

        self.on_toggle_controls(evt=None)

    def on_toggle_controls(self, evt):
        """
        This function enables/disables boxes, depending on the selection
        of the method
        """
        enableList, disableList = [], []
        self.config.iActivationMode = self.activationType.GetStringSelection()
        if self.config.iActivationMode == "Linear":
            enableList = [self.spv_input, self.startVoltage_input, self.endVoltage_input, self.stepVoltage_input]

            disableList = [
                self.exponentialIncrm_input,
                self.exponentialPerct_input,
                self.boltzmann_input,
                self.loadCSVBtn,
            ]
        elif self.config.iActivationMode == "Exponential":
            enableList = [
                self.spv_input,
                self.startVoltage_input,
                self.endVoltage_input,
                self.stepVoltage_input,
                self.exponentialIncrm_input,
                self.exponentialPerct_input,
            ]

            disableList = [self.boltzmann_input, self.loadCSVBtn]
        elif self.config.iActivationMode == "Boltzmann":
            enableList = [
                self.spv_input,
                self.startVoltage_input,
                self.endVoltage_input,
                self.stepVoltage_input,
                self.boltzmann_input,
            ]

            disableList = [self.exponentialIncrm_input, self.exponentialPerct_input, self.loadCSVBtn]
        elif self.config.iActivationMode == "User-defined":
            enableList = [self.loadCSVBtn]
            disableList = [
                self.spv_input,
                self.startVoltage_input,
                self.endVoltage_input,
                self.stepVoltage_input,
                self.exponentialIncrm_input,
                self.exponentialPerct_input,
                self.boltzmann_input,
            ]

        # Since whenever we change the activation zone, polarity or activation
        # type, the wrensCMD is going to be incorrect. It needs to be cleared-up
        # to ensure it is the correct command.
        for item in enableList:
            item.Enable()
        for item in disableList:
            item.Disable()
