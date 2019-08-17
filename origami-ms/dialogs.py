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
import logging

import wx

logger = logging.getLogger("origami")


def dlgBox(exceptionTitle="", exceptionMsg="", type="Error"):
    """Generic message box"""

    logger_obj = logger.info
    if type == "Error":
        dlgStyle = wx.OK | wx.ICON_ERROR
        logger_obj = logger.error
    elif type == "Info":
        dlgStyle = wx.OK | wx.ICON_INFORMATION
    elif type == "Stop":
        dlgStyle = wx.OK | wx.ICON_STOP
    elif type == "Warning":
        dlgStyle = wx.OK | wx.ICON_EXCLAMATION
        logger_obj = logger.warning
    elif type == "Question":
        dlgStyle = wx.YES_NO | wx.ICON_QUESTION

    dlg = wx.MessageDialog(None, exceptionMsg, exceptionTitle, dlgStyle)
    result = dlg.ShowModal()

    # log message
    logger_obj(exceptionMsg)

    if type == "Question":
        return result


def dlgAsk(message="", defaultValue=""):
    """Ask for user input"""
    dlg = wx.TextEntryDialog(None, message, defaultValue=defaultValue)  # parent
    dlg.ShowModal()
    result = dlg.GetValue()
    dlg.Destroy()
    return result
