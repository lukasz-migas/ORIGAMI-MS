# Frequently Asked Questions

## The calculated acquisition time does not match the run time

By default, each of the ORIGAMI-MS methods acquireds a couple of extra scans at the begining and end of the activation period. The `reporter` regions are approx. 3 scans each, however, at the end of the run additional couple of scans are added to complete the acquisition loop. Typically, the number of extra scans is equal to the number of scans per voltage for the last activation step.

## Why does my scan time has to match between ORIGAMI-MS and MassLynx

The reason for this is quite simple. Each of the scripts uses something called Property Banks which are
available in WREnS. These operate by pinging and setting parameters based on scan numbers. If the
scan time is 5 s in MassLynx but only 1 s in ORIGAMI-MS then by the time single scan has finished in
MassLynx, ORIGAMI would have thought that 5 have passed and therefore, the activation ramp would
be completely ignored as the applied voltages would be in a mess. Alternatively, if the scan time in
ORIGAMI is 5 s but only 1 s in MassLynx, then 5 scans would have passed in MassLynx but the activation
ramp would have only progressed by one scan. The second scenario is less ‘bad’ since for each one
scan in ORIGAMI we would have 5 scans in the MassLynx .raw file so in during analysis, we would just
have to multiple the number of scans per voltage by the division of (set scan time/real scan time) –
bear in mind, that this would only work if the values were divisible! In the first scenario, there would
be no possible recovery, as there would not be sufficient number of scans to perform any analysis on,
since for each one MassLynx scan, there could have been multiple activation steps taken. Ideally, both
cases should be avoided!

## Why should I save my parameters

At the moment ORIGAMI-MS (nor ORIGAMI-ANALYSE) is clever enough to know what parameters were used during the acquisition from simply looking at MassLynx .raw files. If you keep track of your parameters, the analysis should be straightforward. We recommend that you save your parameters using the `Save parameters` button to `origami.conf` file directly into the MassLynx .raw folder. Otherwise, just write them down in your notebook.
