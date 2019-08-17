import logging
import os
from subprocess import Popen

import dialogs
import numpy as np
import wx
from exception import MessageError

logger = logging.getLogger("origami")


class data_handling:
    def __init__(self, presenter, view, config):

        self.presenter = presenter
        self.view = view
        self.config = config

    def on_update_wrens_path(self, evt):
        """Update WREnS script path"""

        # get default
        dirname, __ = os.path.split(self.config.wrensRunnerPath)

        dlg = wx.FileDialog(
            self.view,
            "Find WREnS runner (ScriptRunnerLight.exe)",
            wildcard="*.exe",
            style=wx.FD_DEFAULT_STYLE | wx.FD_CHANGE_DIR,
        )

        if os.path.isdir(dirname):
            dlg.SetPath(dirname)

        if dlg.ShowModal() == wx.ID_OK:
            fileName = dlg.GetPath()

            self.config.wrensRunnerPath = fileName
            self.config.update_wrens_paths(True)

    def on_start_wrens_runner(self, evt):
        """Start WREnS runner"""
        if self.config.wrensCMD is None:
            msg = "Are you sure you filled in correct details or pressed calculate?"
            dialogs.dlgBox(
                exceptionTitle="Please complete all necessary fields and press Calculate",
                exceptionMsg=msg,
                type="Error",
            )
            return

        # A couple of checks to ensure the method in the settings is the one
        # currently available in memory..
        if self.config.wrensInput.get("polarity", None) != self.config.iPolarity:
            msg = "The polarity of the current method and the one in the window do not agree. Consider re-calculating."
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            return
        if self.config.wrensInput.get("activationZone", None) != self.config.iActivationZone:
            msg = (
                "The activation zone of the current method and the one in the window do not agree."
                + " Consider re-calculating."
            )
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            return
        if self.config.wrensInput.get("method", None) != self.config.iActivationMode:
            msg = (
                "The acquisition mode of the current method and the one in the window do not agree."
                + " Consider re-calculating."
            )
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            return
        if self.config.wrensInput.get("command", None) != self.config.wrensCMD:
            msg = (
                "The command in the memory and the current method and the one in the window do not agree."
                + " Consider re-calculating."
            )
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            return

        if not os.path.isfile(self.config.wrensRunnerPath):
            raise MessageError(
                "Path does not exist",
                "It would appear that the path to WREnS script runner does not exists."
                + f"\nAre you sure that the script is found here: \n\n{self.config.wrensLinearPath} ",
            )

        logger.info("".join(["Your code: ", self.config.wrensCMD]))

        self.config.wrensRun = Popen(self.config.wrensCMD)

    def on_stop_wrens_runner(self, evt):
        """Stop WREnS script"""

        if self.config.wrensRun:
            logger.info("Stopped acquisition and reset the property banks")
            self.config.wrensRun.kill()
            self.config.wrensReset = Popen(self.config.wrensResetPath)
            self.view.panelControls.goBtn.Enable()
        else:
            raise MessageError(
                "Start acquisition first", "In order to stop WREnS runner, you have to start acquisition first"
            )

    def on_check_parameters(self):
        """This function checks that all variables are in correct format"""

        if not isinstance(self.config.iSPV, int):
            raise MessageError("Incorrect input", "SPV value should be an integer!")

        if not isinstance(self.config.iScanTime, (int, float)):
            raise MessageError("Incorrect input", "Scan time value should be an integer or float!")

        if not isinstance(self.config.iStartVoltage, (int, float)):
            raise MessageError("Incorrect input", "Start voltage should be an integer or float!")

        if not isinstance(self.config.iEndVoltage, (int, float)):
            raise MessageError("Incorrect input", "End voltage should be an integer or float!")

        if not isinstance(self.config.iStepVoltage, (int, float)):
            raise MessageError("Incorrect input", "Step voltage should be an integer or float!")

        if self.config.iActivationMode == "Exponential":
            if not isinstance(self.config.iExponentPerct, (int, float)):
                raise MessageError("Incorrect input", "Exponential % value should be an integer or float!")

            if not isinstance(self.config.iExponentIncre, (int, float)):
                raise MessageError("Incorrect input", "Exponential increment value should be an float!")

        elif self.config.iActivationMode == "Boltzmann":
            if not isinstance(self.config.iBoltzmann, (int, float)):
                raise MessageError("Incorrect input", "Boltzmann offset value should be an integer or float!")

        if abs(self.config.iEndVoltage) <= abs(self.config.iStartVoltage):
            raise MessageError("Incorrect input", "End voltage has to be larger than starting voltage")

        if abs(self.config.iEndVoltage) > 200:
            msg = "The highest possible voltage is 200 V. Set to default: 200"
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            self.config.iEndVoltage = 200
            self.view.panelControls.endVoltage_input.SetValue(str(self.config.iEndVoltage))

        if abs(self.config.iStartVoltage) < 0:
            msg = "The lowest possible voltage is 0 V. Set to default: 0"
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            self.config.iStartVoltage = 0
            self.view.panelControls.startVoltage_input.SetValue(str(self.config.iStartVoltage))

        if self.config.iSPV <= 0:
            msg = "SPV must be larger than 0! Set to default: 3"
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            self.config.iSPV = 3
            self.view.panelControls.spv_input.SetValue(str(self.config.iSPV))

        if self.config.iScanTime <= 0:
            msg = "Scan time must be larger than 0! Set to default: 5"
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            self.config.iScanTime = 5
            self.view.panelControls.scanTime_input.SetValue(str(self.config.iScanTime))

        if self.config.iActivationMode == "Exponential":
            if self.config.iExponentPerct < 0:
                msg = "Exponential % must be larger or equal to 0! Set to default: 0"
                dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
                self.config.iExponentPerct = 0
            elif self.config.iExponentPerct >= 100:
                msg = "Exponential % must be smaller than 100! Set to default: 0"
                dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
                self.config.iExponentPerct = 0
            self.view.panelControls.exponentialPerct_input.SetValue(str(self.config.iExponentPerct))

            if self.config.iExponentIncre <= 0:
                msg = "Exponential increment must be larger than 0! Set to default: 0.01"
                dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
                self.config.iExponentIncre = 0.01
            elif self.config.iExponentIncre > 0.075:
                msg = "Exponential increment must be smaller than 0.075! Set to default: 0.075"
                dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
                self.config.iExponentIncre = 0.075
            self.view.panelControls.exponentialIncrm_input.SetValue(str(self.config.iExponentIncre))
        elif self.config.iActivationMode == "Boltzmann":
            if self.config.iBoltzmann < 10:
                msg = "Boltzmann offset must be larger than 10! Set to default: 10"
                dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
                self.config.iBoltzmann = 10
            elif self.config.iBoltzmann >= 100:
                msg = "Boltzmann offset must be smaller than 100! Set to default: 25"
                dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
                self.config.iBoltzmann = 25
            self.view.panelControls.boltzmann_input.SetValue(str(self.config.iBoltzmann))

        # All good
        return True

    def on_calculate_parameters(self, evt):
        """
        This function is to be used to setup path to save origami parameters
        """

        if not self.config.iActivationMode == "User-defined":
            if self.on_check_parameters() is False:
                logger.info("Please fill in all necessary fields first!")
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
            self.config.wrensInput, ColEnergyX, scanPerVoltageList, timeList, totalAcqTime, start_end_cv_list = (
                self.on_calculate_linear_method()
            )
        elif self.config.iActivationMode == "Exponential":
            self.config.wrensInput, ColEnergyX, scanPerVoltageList, timeList, totalAcqTime, start_end_cv_list = (
                self.on_calculate_exponential_method()
            )
        elif self.config.iActivationMode == "Boltzmann":
            self.config.wrensInput, ColEnergyX, scanPerVoltageList, timeList, totalAcqTime, start_end_cv_list = (
                self.on_calculate_boltzmann_method()
            )
        elif self.config.iActivationMode == "User-defined":
            self.config.wrensInput, ColEnergyX, scanPerVoltageList, timeList, totalAcqTime, start_end_cv_list = (
                self.on_calculate_user_list_method()
            )

        # calculate scans / voltages
        scans, voltages = self.generate_extraction_windows(start_end_cv_list)

        # Setup status:
        self.view.SetStatusText(f"Acq. time: {totalAcqTime:.2f} mins", number=0)
        self.view.SetStatusText(f"{len(scanPerVoltageList):d} steps", number=1)

        # Add wrensCMD to config file
        self.config.wrensCMD = self.config.wrensInput.get("command", None)

        self.view.panelPlots.on_plot_spv(ColEnergyX, scanPerVoltageList)
        self.view.panelPlots.on_plot_time(ColEnergyX, timeList)
        self.view.panelPlots.on_plot_collision_voltages(scans, voltages)
        logger.info(f"Your submission code: {self.config.wrensCMD}")

    def check_acquisition_time(self, acq_time):
        # hard error
        if acq_time > 600:
            raise MessageError(
                "Very long acquisition",
                f"The acquisition will take more than 10 hours ({acq_time / 60:.2f}). Consider reducing "
                + "your collision voltage range or adjusting the parameters!",
            )
        # soft warning
        if acq_time > 300:
            msg = (
                "The acquisition will take more than 5 hours. Consider reducing "
                "your collision voltage range or adjusting the parameters!"
            )
            dialogs.dlgBox(exceptionTitle="Very long acquisition warning", exceptionMsg=msg, type="Warning")

    def check_polarity(self):
        """Get polarity"""
        polarity = "-VE"
        if self.config.iPolarity == "POSITIVE":
            polarity = "+VE"

        return polarity

    def generate_extraction_windows(self, start_end_cv_list):
        start_end_cv_list = np.asarray(start_end_cv_list)

        start_scan = start_end_cv_list[:, 0]
        end_scan = start_end_cv_list[:, 1]
        cv_list = start_end_cv_list[:, 2]

        scans, voltages = [], []
        for i, cv in enumerate(cv_list):
            scans.append(start_scan[i])
            scans.append(end_scan[i])

            voltages.append(cv)
            voltages.append(cv)

        return scans, voltages

    def on_calculate_linear_method(self):
        """Calculate parameters for linear method"""

        startScansPerVoltage = self.config.iSPV
        spv_list, time_list = [], []
        start_time, approx_start_time = 3, 3

        # calculate number of steps
        n_voltages = int((self.config.iEndVoltage - self.config.iStartVoltage) / self.config.iStepVoltage + 1)
        cv_list = np.linspace(self.config.iStartVoltage, self.config.iEndVoltage, n_voltages)

        # simulate generating cv vs scan
        x1 = 0
        start_end_cv_list = []
        for _, cv in enumerate(cv_list):
            x2 = int(x1 + startScansPerVoltage)
            start_end_cv_list.append([x1 + start_time, x2 + start_time, cv])
            spv_list.append(startScansPerVoltage)
            approx_start_time = approx_start_time + startScansPerVoltage
            time_list.append(approx_start_time * self.config.iScanTime)
            x1 = x2

        n_cv_scans = n_voltages * self.config.iSPV
        total_acq_time = round(float((6 + n_cv_scans + self.config.iSPV) * self.config.iScanTime) / 60, 2)
        self.check_acquisition_time(total_acq_time)

        wrens_cmd = "".join(
            [
                self.config.wrensLinearPath,
                self.config.iActivationZone,
                ",",
                self.config.iPolarity,
                ",",
                str(self.config.iSPV),
                ",",
                str(self.config.iScanTime),
                ",",
                str(self.config.iStartVoltage),
                ",",
                str(self.config.iEndVoltage),
                ",",
                str(self.config.iStepVoltage),
                ",",
                str(total_acq_time),
            ]
        )
        wrens_input = {
            "polarity": self.config.iPolarity,
            "activationZone": self.config.iActivationZone,
            "method": self.config.iActivationMode,
            "command": wrens_cmd,
        }

        polarity = self.check_polarity()
        self.view.SetStatusText(
            "".join(
                [
                    "Current method: ",
                    polarity,
                    " mode in the ",
                    self.config.iActivationZone,
                    " using the ",
                    self.config.iActivationMode,
                    " method",
                ]
            ),
            number=2,
        )
        return wrens_input, cv_list, spv_list, time_list, total_acq_time, start_end_cv_list

    def on_calculate_exponential_method(self):
        """Calculate parameters for exponential method"""

        startScansPerVoltage = self.config.iSPV
        scans_per_voltage_list, time_list = [], []
        timeFit = 3
        start_scan = 3
        expAccumulator = 0

        n_voltages = (self.config.iEndVoltage - self.config.iStartVoltage) / self.config.iStepVoltage + 1
        cv_list = np.linspace(self.config.iStartVoltage, self.config.iEndVoltage, n_voltages)
        for i in range(int(n_voltages)):
            if abs(cv_list[i]) >= abs(self.config.iEndVoltage * self.config.iExponentPerct / 100):
                expAccumulator = expAccumulator + self.config.iExponentIncre
                scans_per_voltage_fit = np.round(startScansPerVoltage * np.exp(expAccumulator), 0)
            else:
                scans_per_voltage_fit = startScansPerVoltage

            scans_per_voltage_list.append(scans_per_voltage_fit)
            timeFit = timeFit + scans_per_voltage_fit
            time_list.append(timeFit * self.config.iScanTime)

        x1 = 0
        start_end_cv_list = []
        for i, cv in zip(scans_per_voltage_list, cv_list):
            x2 = int(x1 + i)
            start_end_cv_list.append([x1 + start_scan, x2 + start_scan, cv])
            x1 = x2  # set new starting index

        n_cv_scans = sum(scans_per_voltage_list)
        total_acq_time = round(float((6 + n_cv_scans + self.config.iSPV) * self.config.iScanTime) / 60, 2)
        self.check_acquisition_time(total_acq_time)

        wrens_cmd = "".join(
            [
                self.config.wrensExponentPath,
                self.config.iActivationZone,
                ",",
                self.config.iPolarity,
                ",",
                str(self.config.iSPV),
                ",",
                str(self.config.iScanTime),
                ",",
                str(self.config.iStartVoltage),
                ",",
                str(self.config.iEndVoltage),
                ",",
                str(self.config.iStepVoltage),
                ",",
                str(self.config.iExponentPerct),
                ",",
                str(self.config.iExponentIncre),
                ",",
                str(total_acq_time),
            ]
        )

        wrens_input = {
            "polarity": self.config.iPolarity,
            "activationZone": self.config.iActivationZone,
            "method": self.config.iActivationMode,
            "command": wrens_cmd,
        }

        polarity = self.check_polarity()
        self.view.SetStatusText(
            "".join(
                [
                    "Current method: ",
                    polarity,
                    " mode in the ",
                    self.config.iActivationZone,
                    " using the ",
                    self.config.iActivationMode,
                    " method",
                ]
            ),
            number=2,
        )
        return wrens_input, cv_list, scans_per_voltage_list, time_list, total_acq_time, start_end_cv_list

    def on_calculate_boltzmann_method(self):
        startScansPerVoltage = self.config.iSPV
        scans_per_voltage_list, time_list = [], []
        start_scan = 3
        timeFit = 3
        A1 = 2
        A2 = 0.07
        x0 = 47

        n_voltages = int((self.config.iEndVoltage - self.config.iStartVoltage) / self.config.iStepVoltage + 1)
        cv_list = np.linspace(self.config.iStartVoltage, self.config.iEndVoltage, n_voltages)

        for i in range(int(n_voltages)):
            scans_per_voltage_fit = np.round(
                1 / (A2 + (A1 - A2) / (1 + np.exp((cv_list[i] - x0) / self.config.iBoltzmann))), 0
            )
            scans_per_voltage_list.append(scans_per_voltage_fit * startScansPerVoltage)
            timeFit = timeFit + scans_per_voltage_fit
            time_list.append(timeFit * self.config.iScanTime)

        x1 = 0
        start_end_cv_list = []
        for i, cv in zip(scans_per_voltage_list, cv_list):
            x2 = int(x1 + i)
            start_end_cv_list.append([x1 + start_scan, x2 + start_scan, cv])
            x1 = x2

        n_cv_scans = sum(scans_per_voltage_list)
        total_acq_time = round(float((6 + n_cv_scans + self.config.iSPV) * self.config.iScanTime) / 60, 2)
        self.check_acquisition_time(total_acq_time)

        wrens_cmd = "".join(
            [
                self.config.wrensBoltzmannPath,
                self.config.iActivationZone,
                ",",
                self.config.iPolarity,
                ",",
                str(self.config.iSPV),
                ",",
                str(self.config.iScanTime),
                ",",
                str(self.config.iStartVoltage),
                ",",
                str(self.config.iEndVoltage),
                ",",
                str(self.config.iStepVoltage),
                ",",
                str(self.config.iBoltzmann),
                ",",
                str(total_acq_time),
            ]
        )

        wrens_input = {
            "polarity": self.config.iPolarity,
            "activationZone": self.config.iActivationZone,
            "method": self.config.iActivationMode,
            "command": wrens_cmd,
        }
        polarity = self.check_polarity()
        self.view.SetStatusText(
            "".join(
                [
                    "Current method: ",
                    polarity,
                    " mode in the ",
                    self.config.iActivationZone,
                    " using the ",
                    self.config.iActivationMode,
                    " method",
                ]
            ),
            number=2,
        )
        return wrens_input, cv_list, scans_per_voltage_list, time_list, total_acq_time, start_end_cv_list

    def on_calculate_user_list_method(self):

        if self.config.CSVFilePath is None:
            msg = "Please load a CSV file first."
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            return
        if self.config.iScanTime is None or self.config.iScanTime == "":
            msg = "Please fill in appropriate fields. The scan time is empty or incorrect"
            dialogs.dlgBox(exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error")
            return

        try:
            spvCVlist = np.genfromtxt(self.config.CSVFilePath, skip_header=1, delimiter=",", filling_values=0)
        except BaseException:
            return
        # Read table
        scans_per_voltage_list = spvCVlist[:, 0].astype(int)
        cv_list = spvCVlist[:, 1]

        timeFit = 3
        time_list = []
        for i in scans_per_voltage_list:
            timeFit = timeFit + i
            time_list.append(timeFit * self.config.iScanTime)

        if len(scans_per_voltage_list) != len(cv_list):
            return

        start_scan = 3
        x1 = 0
        start_end_cv_list = []
        for i, cv in zip(scans_per_voltage_list, cv_list):
            x2 = int(x1 + i)
            start_end_cv_list.append([x1 + start_scan, x2 + start_scan, cv])
            x1 = x2

        total_acq_time = np.round((sum(scans_per_voltage_list) * self.config.iScanTime) / 60, 2)
        if total_acq_time > 300:
            msg = (
                "The acquisition will take more than 5 hours. Consider reducing "
                "your collision voltage range or adjusting the parameters!"
            )
            dialogs.dlgBox(exceptionTitle="Very long acquisition warning", exceptionMsg=msg, type="Warning")

        SPV_list = " ".join(str(spv) for spv in scans_per_voltage_list.tolist())
        SPV_list = "".join(["[", SPV_list, "]"])
        CV_list = " ".join(str(cv) for cv in cv_list.tolist())
        CV_list = "".join(["[", CV_list, "]"])

        self.config.SPVsList = scans_per_voltage_list
        self.config.CVsList = cv_list

        wrens_cmd = "".join(
            [
                self.config.wrensUserDefinedPath,
                self.config.iActivationZone,
                ",",
                self.config.iPolarity,
                ",",
                str(self.config.iScanTime),
                ",",
                SPV_list,
                ",",
                CV_list,
            ]
        )

        wrens_input = {
            "polarity": self.config.iPolarity,
            "activationZone": self.config.iActivationZone,
            "method": self.config.iActivationMode,
            "command": wrens_cmd,
        }

        polarity = self.check_polarity()
        self.view.SetStatusText(
            "".join(
                [
                    "Current method: ",
                    polarity,
                    " mode in the ",
                    self.config.iActivationZone,
                    " using the ",
                    self.config.iActivationMode,
                    " method",
                ]
            ),
            number=2,
        )
        return wrens_input, cv_list, scans_per_voltage_list, time_list, total_acq_time, start_end_cv_list
