import numpy as np

__all__ = ["byte2str", "str2num", "num2str", "str2int", "float2int", "str2bool"]


def str2num(string):
    try:
        val = float(string)
        return val
    except (ValueError, TypeError):
        return None


def num2str(val):
    try:
        string = str(val)
        return string
    except (ValueError, TypeError):
        return None


def str2int(string):
    try:
        val = int(string)
        return val
    except (ValueError, TypeError):
        return None


def float2int(num):
    try:
        val = int(num)
        return val
    except (ValueError, TypeError):
        return num


def isempty(input):
    try:
        if np.asarray(input).size == 0 or input is None:
            out = True
        else:
            out = False
    except (TypeError, ValueError, AttributeError):
        print("Could not determine whether object is empty. Output set to FALSE")
        out = False
    return out


def str2bool(s):
    if s == "True":
        return True
    elif s == "False":
        return False
    else:
        raise ValueError
