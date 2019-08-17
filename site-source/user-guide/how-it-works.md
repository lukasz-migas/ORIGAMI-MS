# How it works

ORIGAMI-MS works by interfacing MassLynx and Waters Research Enabled Software (**WREnS**) to carry
out a typically tedious task of increasing the collision or cone voltage prior to ion mobility separation.

The program works by executing a pre-compiled C# code alongside normal acquisition, however the
C# (WREnS code) modifies some of the DC potentials on the instrument, taking control away from
MassLynx. In ORIGAMI-MS case, we only control three DC potentials, the `DRE` lens which controls the
attenuation of the ion beam, the sample cone voltage (`SAMPLE_CONE_VOLTAGE_SETTING`) and trap
collision voltage (`SOURCE_BIAS_SETTING`). These are modified on-the-fly, as the acquisition continues,
to reflect the user settings. The latter two can be controlled in voltage range of 0 to 200 V, which
provides sufficient activation energy to unfold and fragment most compounds.

!!! Note
    Some instruments have been modified to have wider activation range. If this is you, please let me know and I can
    modify the maximum voltage value.
