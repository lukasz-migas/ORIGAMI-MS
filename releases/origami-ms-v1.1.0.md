# Update

The latest version of ORIGAMI-MS with various improvements and fixes.

There are no changes to the underlying algorithms using by ORIGAMI-MS.

## Pre-release warning

This is a pre-released version of ORIGAMI-MS. I am yet to fully test it on a PC connected to an instrument, so bare that in mind!

## What changed

### Code base

- CHANGED: updated to Python 3.7
- CHANGED: updated to wxPython 4.0.6
- NEW: ORIGAMI-MS is put through travisCI pipeline to make sure it runs smoothly
- IMPROVED: migrated a lot of code away from the `presenter` class to allow better debugging

### User interface

- IMPROVED: user interface was refreshed by reorganizing moving components around
- IMPROVED: the `Log` panel was removed in place of a integrated logger which writes directly to file (found in `logs\` directory). In order to see the current messages, have at the accompanied command window
- NEW: added new plot `Collision voltage steps` which plots scans versus collision voltage, clearly showing size of each step
- NEW: added `Copy plot to clipboard` when you right-click in the plot area
- IMPROVED: you can now zoom-in in any of the plots by clicking and dragging in the plot area
- NEW: added menu shortcut to view ORIGAMI-MS documentation (available at [origami-ms.lukasz-migas.com]([origami-ms.lukasz-migas.com](https://origami-ms.lukasz-migas.com/)))
- NEW: added menu shortcut to the GitHub webpage

## Documentation

I have rewritten and updated ORIGAMI-MS documentation, which can be found online from now on. Please visit [origami-ms.lukasz-migas.com](https://origami-ms.lukasz-migas.com/) for the most up-to-date version.

## How to update

The best way to update is to download the zipped folder, unpack it on your instrument PC and start running. Please let me know if you encounter any problems.

Many thanks,
Lukasz
