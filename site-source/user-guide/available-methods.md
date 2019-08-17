# Available methods

There are three built-in methods in ORIGAMI-MS, namely `linear`, `boltzmann` and `exponential` which have been designed
around improving the quality of CIU/aIMS acquired data. The final method, `user-defined` allows usage of arbirary
lists of scans per voltage and collision voltages, giving you all the freedom you should need.

## Linear

The `linear` method follows simple priciple of having the same number of scans for each collision voltage increment.
This makes the acquisition and analysis very straightforward, however, can have detrimental effect on the overall quality
of the data when signal-to-noise ratios go down.

![Linear method](../../assets/origami-ms-linear.png)

## Exponential

The `exponential` method uses an exponential model to systematically increase the number of scans as the collision voltage
increases, which can improve data quality. This of course, will lead to longer acquisition times.

![Exponential method](../../assets/origami-ms-exponential.png)

## Boltzmann

The `boltzmann` method uses a Boltzmann equation to model systematically increase the number of scans as the collision voltage
increases, which can improve data quality. This of course, will lead to longer acquisition times.

![Boltzmann method](../../assets/origami-ms-boltzmann.png)

## User-defined

As the suggests, you define your own parameters which will be used during the data acquisition.
See [example file](https://github.com/lukasz-migas/ORIGAMI-MS/blob/master/origami-ms/sample/ciu_list.csv)
for inspiration in what should be included in the CSV file.

![User-defined method](../../assets/origami-ms-user-defined.png)
