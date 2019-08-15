import dialogs
from exception import MessageError
import numpy as np


class data_handling:

    def __init__(self, presenter, view, config,):

        self.presenter = presenter
        self.view = view
        self.config = config

    def onCheckParameters(self):
        """This function checks that all variables are in correct format"""

        if not isinstance(self.config.iSPV, int):
            raise MessageError("Incorrect input",
                               "SPV value should be an integer!"
                               )

        if not isinstance(self.config.iScanTime, (int, float)):
            raise MessageError("Incorrect input",
                               "Scan time value should be an integer or float!"
                               )

        if not isinstance(self.config.iStartVoltage, (int, float)):
            raise MessageError("Incorrect input",
                               "Start voltage should be an integer or float!"
                               )

        if not isinstance(self.config.iEndVoltage, (int, float)):
            raise MessageError("Incorrect input",
                               "End voltage should be an integer or float!"
                               )

        if not isinstance(self.config.iStepVoltage, (int, float)):
            raise MessageError("Incorrect input",
                               "Step voltage should be an integer or float!"
                               )

        if self.config.iActivationMode == "Exponential":
            if not isinstance(self.config.iExponentPerct, (int, float)):
                raise MessageError("Incorrect input",
                                   "Exponential % value should be an integer or float!"
                                   )

            if not isinstance(self.config.iExponentIncre, (int, float)):
                raise MessageError("Incorrect input",
                                   "Exponential increment value should be an float!"
                                   )

        elif self.config.iActivationMode == "Boltzmann":
            if not isinstance(self.config.iBoltzmann, (int, float)):
                raise MessageError("Incorrect input",
                                   "Boltzmann offset value should be an integer or float!"
                                   )

        if abs(self.config.iEndVoltage) <= abs(self.config.iStartVoltage):
            raise MessageError("Incorrect input",
                               "End voltage has to be larger than starting voltage"
                               )

        if abs(self.config.iEndVoltage) > 200:
            msg = "The highest possible voltage is 200 V. Set to default: 200"
            dialogs.dlgBox(
                exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error"
            )
            self.config.iEndVoltage = 200
            self.view.panelControls.endVoltage_input.SetValue(
                str(self.config.iEndVoltage)
            )

        if abs(self.config.iStartVoltage) < 0:
            msg = "The lowest possible voltage is 0 V. Set to default: 0"
            dialogs.dlgBox(
                exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error"
            )
            self.config.iStartVoltage = 0
            self.view.panelControls.startVoltage_input.SetValue(
                str(self.config.iStartVoltage)
            )

        if self.config.iSPV <= 0:
            msg = "SPV must be larger than 0! Set to default: 3"
            dialogs.dlgBox(
                exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error"
            )
            self.config.iSPV = 3
            self.view.panelControls.spv_input.SetValue(str(self.config.iSPV))

        if self.config.iScanTime <= 0:
            msg = "Scan time must be larger than 0! Set to default: 5"
            dialogs.dlgBox(
                exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error"
            )
            self.config.iScanTime = 5
            self.view.panelControls.scanTime_input.SetValue(
                str(self.config.iScanTime))

        if self.config.iActivationMode == "Exponential":
            if self.config.iExponentPerct < 0:
                msg = "Exponential % must be larger or equal to 0! Set to default: 0"
                dialogs.dlgBox(
                    exceptionTitle="Mistake in the input",
                    exceptionMsg=msg,
                    type="Error",
                )
                self.config.iExponentPerct = 0
            elif self.config.iExponentPerct >= 100:
                msg = "Exponential % must be smaller than 100! Set to default: 0"
                dialogs.dlgBox(
                    exceptionTitle="Mistake in the input",
                    exceptionMsg=msg,
                    type="Error",
                )
                self.config.iExponentPerct = 0
            self.view.panelControls.exponentialPerct_input.SetValue(
                str(self.config.iExponentPerct)
            )

            if self.config.iExponentIncre <= 0:
                msg = (
                    "Exponential increment must be larger than 0! Set to default: 0.01"
                )
                dialogs.dlgBox(
                    exceptionTitle="Mistake in the input",
                    exceptionMsg=msg,
                    type="Error",
                )
                self.config.iExponentIncre = 0.01
            elif self.config.iExponentIncre > 0.075:
                msg = "Exponential increment must be smaller than 0.075! Set to default: 0.075"
                dialogs.dlgBox(
                    exceptionTitle="Mistake in the input",
                    exceptionMsg=msg,
                    type="Error",
                )
                self.config.iExponentIncre = 0.075
            self.view.panelControls.exponentialIncrm_input.SetValue(
                str(self.config.iExponentIncre)
            )
        elif self.config.iActivationMode == "Boltzmann":
            if self.config.iBoltzmann < 10:
                msg = "Boltzmann offset must be larger than 10! Set to default: 10"
                dialogs.dlgBox(
                    exceptionTitle="Mistake in the input",
                    exceptionMsg=msg,
                    type="Error",
                )
                self.config.iBoltzmann = 10
            elif self.config.iBoltzmann >= 100:
                msg = "Boltzmann offset must be smaller than 100! Set to default: 25"
                dialogs.dlgBox(
                    exceptionTitle="Mistake in the input",
                    exceptionMsg=msg,
                    type="Error",
                )
                self.config.iBoltzmann = 25
            self.view.panelControls.boltzmann_input.SetValue(
                str(self.config.iBoltzmann)
            )

        # All good
        return True

    def check_acquisition_time(self, acq_time):
        # hard error
        if acq_time > 600:
            raise MessageError(
                "Very long acquisition",
                f"The acquisition will take more than 10 hours ({acq_time / 60:.2f}). Consider reducing " +
                "your collision voltage range or adjusting the parameters!"
                               )
        # soft warning
        if acq_time > 300:
            msg = (
                "The acquisition will take more than 5 hours. Consider reducing "
                "your collision voltage range or adjusting the parameters!"
            )
            dialogs.dlgBox(
                exceptionTitle="Very long acquisition warning",
                exceptionMsg=msg,
                type="Warning",
            )

    def onPrepareLinearMethod(self):

        startScansPerVoltage = self.config.iSPV
        spv_list, time_list = [], []
        approx_start_time = 3

        # calculate number of steps
        n_voltages = int((self.config.iEndVoltage - self.config.iStartVoltage) / self.config.iStepVoltage + 1)
        cv_list = np.linspace(self.config.iStartVoltage, self.config.iEndVoltage, n_voltages)
        for __ in range(n_voltages):
            spv_list.append(startScansPerVoltage)
            approx_start_time = approx_start_time + startScansPerVoltage
            time_list.append(approx_start_time * self.config.iScanTime)

        print(time_list)

        n_cv_scans = n_voltages * self.config.iSPV
        total_acq_time = round(
            float((6 + n_cv_scans + self.config.iSPV)
                  * self.config.iScanTime)
            / 60,
            2,
        )
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
        if self.config.iPolarity == "POSITIVE":
            polarity = "+VE"
        else:
            polarity = "-VE"
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
        return wrens_input, cv_list, spv_list, time_list, total_acq_time

    def onPrepareExponentialMethod(self):
        startScansPerVoltage = self.config.iSPV
        spv_list, time_list = [], []
        timeFit = 3
        expAccumulator = 0

        n_voltages = (
            self.config.iEndVoltage - self.config.iStartVoltage
        ) / self.config.iStepVoltage + 1
        cv_list = np.linspace(
            self.config.iStartVoltage, self.config.iEndVoltage, n_voltages
        )
        for i in range(int(n_voltages)):
            if abs(cv_list[i]) >= abs(
                self.config.iEndVoltage * self.config.iExponentPerct / 100
            ):
                expAccumulator = expAccumulator + self.config.iExponentIncre
                scanPerVoltageFit = np.round(
                    startScansPerVoltage * np.exp(expAccumulator), 0
                )
            else:
                scanPerVoltageFit = startScansPerVoltage

            spv_list.append(scanPerVoltageFit)
            timeFit = timeFit + scanPerVoltageFit
            time_list.append(timeFit * self.config.iScanTime)

        n_cv_scans = sum(spv_list)
        total_acq_time = round(
            float((6 + n_cv_scans + self.config.iSPV)
                  * self.config.iScanTime)
            / 60,
            2,
        )
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
        if self.config.iPolarity == "POSITIVE":
            polarity = "+VE"
        else:
            polarity = "-VE"
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
        return wrens_input, cv_list, spv_list, time_list, total_acq_time

    def onPrepareBoltzmannMethod(self):
        startScansPerVoltage = self.config.iSPV
        spv_list, time_list = [], []
        timeFit = 3
        A1 = 2
        A2 = 0.07
        x0 = 47

        n_voltages = int(
            (self.config.iEndVoltage - self.config.iStartVoltage)
            / self.config.iStepVoltage
            +1
        )
        cv_list = np.linspace(
            self.config.iStartVoltage, self.config.iEndVoltage, n_voltages
        )
        for i in range(int(n_voltages)):
            scanPerVoltageFit = np.round(1 / (A2 + (A1 - A2) / (1 + np.exp((cv_list[i] - x0) / self.config.iBoltzmann))), 0,)
            spv_list.append(scanPerVoltageFit * startScansPerVoltage)
            timeFit = timeFit + scanPerVoltageFit
            time_list.append(timeFit * self.config.iScanTime)

        n_cv_scans = sum(spv_list)
        total_acq_time = round(float((6 + n_cv_scans + self.config.iSPV)
                  * self.config.iScanTime)
            / 60,
            2,
        )
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
        if self.config.iPolarity == "POSITIVE":
            polarity = "+VE"
        else:
            polarity = "-VE"
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
        return wrens_input, cv_list, spv_list, time_list, total_acq_time

    def onPrepareListMethod(self):

        if self.config.CSVFilePath is None:
            msg = "Please load a CSV file first."
            dialogs.dlgBox(
                exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error"
            )
            return
        if self.config.iScanTime is None or self.config.iScanTime == "":
            msg = (
                "Please fill in appropriate fields. The scan time is empty or incorrect"
            )
            dialogs.dlgBox(
                exceptionTitle="Mistake in the input", exceptionMsg=msg, type="Error"
            )
            return

        try:
            spvCVlist = np.genfromtxt(
                self.config.CSVFilePath, skip_header=1, delimiter=",", filling_values=0
            )
        except BaseException:
            return
        # Read table
        spv_list = spvCVlist[:, 0].astype(int)
        cv_list = spvCVlist[:, 1]

        timeFit = 3
        time_list = []
        for i in spv_list:
            timeFit = timeFit + i
            time_list.append(timeFit * self.config.iScanTime)

        if len(spv_list) != len(cv_list):
            return

        total_acq_time = np.round(
            (sum(spv_list) * self.config.iScanTime) / 60, 2
        )
        if total_acq_time > 300:
            msg = (
                "The acquisition will take more than 5 hours. Consider reducing "
                "your collision voltage range or adjusting the parameters!"
            )
            dialogs.dlgBox(
                exceptionTitle="Very long acquisition warning",
                exceptionMsg=msg,
                type="Warning",
            )

        SPV_list = " ".join(str(spv) for spv in spv_list.tolist())
        SPV_list = "".join(["[", SPV_list, "]"])
        CV_list = " ".join(str(cv) for cv in cv_list.tolist())
        CV_list = "".join(["[", CV_list, "]"])

        self.config.SPVsList = spv_list
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
        if self.config.iPolarity == "POSITIVE":
            polarity = "+VE"
        else:
            polarity = "-VE"
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
        return wrens_input, cv_list, spv_list, time_list, total_acq_time
