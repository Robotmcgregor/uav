#!/usr/bin/env python
"""
this script runs the image sen2make10bands_image.py script, this enables the script to be run from in a notebook on windows system
Author: Grant Staben
Date: 24/01/2020
"""
from __future__ import print_function, division

# import the requried modules
import sys
import os
import argparse
import pdb
import pandas as pd
import csv
import subprocess
import rasterio
import numpy as np


# command arguments
def getCmdargs():
    """
    Get commandline arguments
    """
    p = argparse.ArgumentParser(description="""
        Create a single stack of Sentinel-2 bands, all at 10m pixel size. Output is a single stack of 10 layers. 
        Bands are out out put as  B1','B2','B3','B4','B5','B6','B7','B8','B9','B10 which is the Sentinel-2 band numbers 
        B02, B03, B04, B08, B05, B06, B07, B08A, B11, B12. 
    """)
    p.add_argument("--directory", help="Name of 10m input file. Expected to have exactly 4 bands.")
    # p.add_argument("--ref20", help="Name of 20m input file.")
    p.add_argument("--outfile", help="Name of output image file")
    cmdargs = p.parse_args()

    if cmdargs.directory is None:
        p.print_help()
        sys.exit()

    return cmdargs


def runscript(directory, outimg):
    """
    call the script and run it.

    """

    cmd = "python composite_multi_bands_image.py --directory %s --outfile %s" % (directory, outimg)

    os.system(cmd)
    print(outimg + ' complete')


def main():
    # calls in the command arguments and runscript function.

    cmdargs = getCmdargs()
    print("init script")

    directory = cmdargs.directory
    #ref20 = cmdargs.ref20
    outimg = cmdargs.outfile

    runscript(directory, outimg)


if __name__ == "__main__":
    main()