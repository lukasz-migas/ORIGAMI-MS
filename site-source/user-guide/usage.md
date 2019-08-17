# Usage

ORIGAMI-MS can be operated using the command line or graphical user interface

## Graphical User Interface - easier of the two

1. Go to ORIGAMI-MS folder
2. Select polarity, activation region, activation method and then fill-in appropriate parameters. If you miss any parameter or the parameter does not match its requirements, you will be prompted to try again.
3. Ensure your parameters are correct by clicking on the `Calculate` button. If everything worked fine, you will see not error messages and the code compiled correctly.
4. Examine one of the three available plots to make sure you are happy.
5. Go to MassLynx tune page and start acquisition. You can either set the acquisition time in MassLynx (make sure to add at least a minute to the run time) or you can come back to ORIGAMI-MS after the pre-calculated amount of time and stop the acquisition.
6. Go back to ORIGAMI-MS and press on `Go` button. If successful, a new window will appear with print out messages.
7. Let it do its thing and come back when the acquisition is finished.
8. Analyse your data in [ORIGAMI-ANALYSE](https://origami.lukasz-migas.com/user-guide/data-handling/automated-ciu)

!!! Important
    Make sure you set the scan time to whatever you've set in ORIGAMI-MS. If you do not, data acquisition will be out of sync and it will be useless.

!!! Important
    If you need to cancel the run, just press on the `Stop` button - this will stop ORIGAMI-MS script. Subsequently, go to MassLynx, stop the acquisition and reinitilize MassLynx.

## Command line interface - quicker of the two

1. Open command prompt and navigate to wherever the WREnS `ScriptRunnerLight.exe` is located. Usually `C:\Program Files (x86)\Wrens\Bin`
2. The general rules are `ScriptRunnerLight.exe SCRIPT_NAME.dll PARAMETERS` where you replace the `SCRIPT_NAME.dll` with whatever method you are using and put in appropriate parameters in the `PARAMETERS` section.

!!! Important
    You can stop the script from running by pressing `CTRL+C` or `CTRL+PAUSE` on your keyboard. To be safe, I would also run the `CIU_RESET.dll` script using the `ScriptRunnerLight.exe CIU_RESET.dll` command.

### Example command line inputs

#### Linear method

```bash
ScriptRunnerLight.exe CIU_LINEAR.dll TRAP,POSITIVE,3,5,4.0,200.0,2.0,25.5
```

- region: TRAP
- polarity: POSITIVE
- SPV: 3
- scan time: 5
- start V: 4
- end V: 200
- step V: 2V
- approx. run time – 25.5 (can be any number!)

#### Exponential method

```bash
ScriptRunnerLight.exe CIU_EXPONENT.dll TRAP,POSITIVE,3,5,4.0,200.0,2.0,20.0,0.03,92.75
```

- region: TRAP
- polarity: POSITIVE
- SPV: 3
- scan time: 5
- start V: 4
- end V: 200
- step V: 2V
- exponential percent - 20
- exponential increment – 0.03
- approx. run time – 92.75 (can be any number!)

#### Boltzmann method

```bash
ScriptRunnerLight.exe CIU_FITTED.dll TRAP,POSITIVE,3,5,4.0,200.0,2.0,50.0,61.25
```

- region: TRAP
- polarity: POSITIVE
- SPV: 3
- scan time: 5
- start V: 4
- end V: 200
- step V: 2V
- Boltzmann offset – 50
- approx. run time – 61.25 (can be any number!)

#### User-defined method

```bash
ScriptRunnerLight.exe CIU_LIST.dll "TRAP,POSITIVE,5, [3 3 3 3 3 3],[4 6 8 10 12 14]
```

- region: TRAP
- polarity: POSITIVE
- scan time: 5
- list of scans per voltage (SPVs): [3 3 3 3 3 3]
- list of collision voltages (CVs): [4 6 8 10 12 14]

!!! Note
    This is probably the hardest method to get right. The parameters must start with quotation
    mark (“) and values cannot be separated by anything other than comma, apart from the values
    inside the square brackets ([ ]) which have to be separated by single space. Of course, the lists of
    SPVs and CVs must of the same length.

!!! Note
    In general, the values inside the PARAMETERS section of the code must not be separated by anything other than a comma (,)

!!! Tip
    Make sure you save the ORIGAMIMS parameters in your notebook, in the header of the MassLynx .raw file or as configuration file inside the MassLynx .raw file. This way, you will make your life a lot easier and your analysis will be swift and pain-free.
