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
# Load libraries
import wx.aui
from IDs import ID_helpCite
from IDs import ID_helpDocumentation
from IDs import ID_helpGitHub
from IDs import ID_helpNewVersion
from IDs import ID_on_export_config
from IDs import ID_on_import_config
from IDs import ID_on_set_masslynx_path
from IDs import ID_on_set_wrens_path
from IDs import ID_SHOW_ABOUT
from origamiStyles import makeMenuItem
from panelAbout import panelAbout
from panelControls import panelControls
from panelPlot import panelPlot


class MyFrame(wx.Frame):
    def __init__(self, parent, config, icons, title="ORIGAMI-MS"):
        wx.Frame.__init__(self, None, title=title, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.SetSize(600, 700)
        self.Centre()

        self.presenter = parent
        self.config = config
        self.icons = icons

        icon = wx.Icon()
        icon.CopyFromBitmap(self.icons.iconsLib["origami_logo_16"])
        self.SetIcon(icon)

        # Setup Notebook manager
        self._mgr = wx.aui.AuiManager(self)
        self._mgr.SetDockSizeConstraint(1, 1)

        self.panelControls = panelControls(self, self.presenter, self.config)  # Settings
        self.panelPlots = panelPlot(self, self.config)  # Settings

        self._mgr.AddPane(
            self.panelControls,
            wx.aui.AuiPaneInfo()
            .Top()
            .CloseButton(False)
            .GripperTop()
            .MinSize((400, 200))
            .Gripper(False)
            .BottomDockable(False)
            .TopDockable(False)
            .CaptionVisible(False)
            .Resizable(False),
        )

        self._mgr.AddPane(
            self.panelPlots,
            wx.aui.AuiPaneInfo()
            .Bottom()
            .CloseButton(False)
            .GripperTop(False)
            .MinSize((500, 400))
            .Gripper(False)
            .BottomDockable(False)
            .TopDockable(False)
            .CaptionVisible(False)
            .Resizable(False),
        )

        # Load other parts
        self._mgr.Update()
        self.make_statusbar()
        self.make_menubar()

        self.Bind(wx.EVT_CLOSE, self.presenter.quit)

    def _setup_after_startup(self):
        """Bind functions after intilization of `data_handling` module"""
        self.Bind(wx.EVT_MENU, self.presenter.data_handling.on_update_wrens_path, id=ID_on_set_wrens_path)

    def make_menubar(self):

        # FILE MENU
        self.mainMenu = wx.MenuBar()
        menuFile = wx.Menu()
        menuFile.Append(ID_on_set_masslynx_path, "Set MassLynx file path\tCtrl+O")
        menuFile.AppendSeparator()
        menuFile.Append(ID_on_set_wrens_path, "Set WREnS runner (ScriptRunnerLight.exe) path")
        menuFile.AppendSeparator()
        menuFile.Append(ID_on_import_config, "Import configuration file\tCtrl+C")
        menuFile.Append(ID_on_export_config, "Export configuration file\tCtrl+Shift+C")

        self.mainMenu.Append(menuFile, "&File")

        # HELP MENU
        menuHelp = wx.Menu()
        menuHelp.Append(ID_helpNewVersion, "Check for updates (online)")
        menuHelp.Append(ID_helpDocumentation, "Open documentation site (online)")
        menuHelp.Append(ID_helpGitHub, "Go to GitHub site (online)")
        menuHelp.Append(ID_helpCite, "Go to ORIGAMI publication site (online)")
        menuHelp.AppendSeparator()
        menuHelp.Append(makeMenuItem(parent=menuHelp, id=ID_SHOW_ABOUT, text="About ORIGAMI\tCtrl+Shift+A"))
        self.mainMenu.Append(menuHelp, "&Help")

        self.SetMenuBar(self.mainMenu)

        self.Bind(wx.EVT_MENU, self.presenter.on_get_masslynx_path, id=ID_on_set_masslynx_path)
        self.Bind(wx.EVT_MENU, self.presenter.on_import_config, id=ID_on_import_config)
        self.Bind(wx.EVT_MENU, self.presenter.on_export_config, id=ID_on_export_config)

        self.Bind(wx.EVT_MENU, self.on_open_about, id=ID_SHOW_ABOUT)
        self.Bind(wx.EVT_MENU, self.presenter.on_open_link, id=ID_helpCite)
        self.Bind(wx.EVT_MENU, self.presenter.on_open_link, id=ID_helpNewVersion)
        self.Bind(wx.EVT_MENU, self.presenter.on_open_link, id=ID_helpDocumentation)
        self.Bind(wx.EVT_MENU, self.presenter.on_open_link, id=ID_helpGitHub)

    def on_open_about(self, evt):
        """Show About mMass panel."""
        about = panelAbout(self, self.presenter, "About ORIGAMI", self.config, self.icons)
        about.Centre()
        about.Show()
        about.SetFocus()

    def make_statusbar(self):
        self.mainStatusbar = self.CreateStatusBar(3, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.mainStatusbar.SetStatusWidths([120, 50, -1])
