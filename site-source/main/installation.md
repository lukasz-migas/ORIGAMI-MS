# Installation

## Package installation

ORIGAMI-MS can be installed either using the pre-compiled version available from GitHub or compile from source

### Pre-compiled

You can download the latest pre-compiled version of ORIGAMI-MS from [GitHub](https://github.com/lukasz-migas/ORIGAMI-MS/releases)

#### Requirements

- Windows 7/8/10
- HDD space: ~100 Mb
- WREnS
- Waters Synapt G2/G2S/G2Si

#### Set-up and installation

Technically, there is no installation. Simply download the latest version of ORIGAMI-MS onto your instrument PC, unzip it and
place it wherever it is convenient. Once unzipped, you simply open the folder and search for file **ORIGAMIMS.exe**
which can be executed by double-clicking on it.

### Source code

#### Requirements

- Windows 7/8/10
- HDD space: ~100 Mb
- WREnS
- Waters Synapt G2/G2S/G2Si
- [Dependencies](https://github.com/lukasz-migas/ORIGAMI-MS/blob/master/origamims_requirements.txt)

#### Set-up and installation from source

You can clone/copy the [GitHub](https://github.com/lukasz-migas/ORIGAMI-MS) directory and only looking at the contents of origami-ms

#### Recommendations

You are best of using conda or python environments to keep your Python installation nice and tidy. In order to create a conda environment, open a command window and type-in

```python
conda create -n origami-ms python=3.7
```

To activate this environment, type-in

```python
activate origami-ms
```

Install all dependencies

```python
pip install -r origamims_requirements.txt
```

To run ORIGAMI from source, type-in

```python
python origamims.py
```

!!! Tip
    Sometimes its better to install wxPython separately

```python
pip install -U wxPython
```

If you have installed all dependancies, you should be good! :)
