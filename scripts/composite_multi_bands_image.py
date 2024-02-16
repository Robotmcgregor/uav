#!/usr/bin/env python
"""
A script to blend all the 10 and the 20m SWIR bands stacks of Sentinel-2 bands into a single
10m stack, it has been modified from Neils qv_sen2makeTM10.py script which only using just the bands which correspond to the Landsat TM bands. 
This produces an image using B02, B03, B04, B08, B11, B12 from the original Sentinel-2 band names 

"""
from __future__ import print_function, division

import sys
import os
from glob import glob
import argparse

import numpy
from osgeo import gdal

from rios import applier
from rios import fileinfo

import pdb

def getCmdargs():
    """
    Get commandline arguments
    """
    p = argparse.ArgumentParser(description="""
        Create a single stack of Sentinel-2 bands, all at 10m pixel size. Output is a single stack of 6 layers. 
        Bands are out put as  B1','B2','B3','B4','B5','B6',which is the Sentinel-2 band numbers 
        B02, B03, B04, B08, B11, B12. 
    """)
    p.add_argument("--directory", help="Name oof the directory containing all 5 greyscale band images.")
    #p.add_argument("--ref20", help="Name of 20m input file.")
    p.add_argument("--outfile", help="Name of output image file")
    cmdargs = p.parse_args()
    
    if cmdargs.directory is None:
        p.print_help()
        sys.exit()
    
    return cmdargs




def mainRoutine():
    """
    Main routine
    """
    print('init composite multi bands image')
    cmdargs = getCmdargs()

    image_path_list = []
    image_list = ["mosaic_blue", "mosaic_green", "mosaic_red", "mosaic_red edge", "mosaic_nir"]
    for n in image_list:

        for i in glob(os.path.join(cmdargs.directory, "*{0}.tif".format(n))):
            print(i)

            if 'transparent' not in i:
                image_path_list.append(i)

    print(image_path_list)


    if len(image_path_list) != 5:
        print('Error - not enough bands located.')
        sys.exit()

       
    infiles = applier.FilenameAssociations()
    outfiles = applier.FilenameAssociations()
    controls = applier.ApplierControls()
    otherargs = applier.OtherInputs()

    infiles.refb = image_path_list[0]
    infiles.refg = image_path_list[1]
    infiles.refr = image_path_list[2]
    infiles.refre = image_path_list[3]
    infiles.refnir = image_path_list[4]


    outfiles.outimg = os.path.join(cmdargs.directory, cmdargs.outfile)

    refbinfo = fileinfo.ImageInfo(image_path_list[0])
    refginfo = fileinfo.ImageInfo(image_path_list[1])
    refrinfo = fileinfo.ImageInfo(image_path_list[2])
    refreinfo = fileinfo.ImageInfo(image_path_list[3])
    refnirinfo = fileinfo.ImageInfo(image_path_list[4])

    otherargs.refbnull = refbinfo.nodataval[0]
    otherargs.refgnull = refginfo.nodataval[0]
    otherargs.refrnull = refrinfo.nodataval[0]
    otherargs.refrenull = refreinfo.nodataval[0]
    otherargs.refnirnull = refnirinfo.nodataval[0]

    controls.setResampleMethod('cubic')
    controls.setReferenceImage(image_path_list[0])
    controls.setStatsIgnore(otherargs.refbnull)

    applier.apply(doMerge, infiles, outfiles, otherargs, controls=controls)

def doMerge(info, inputs, outputs, otherargs):
    """
    Merge the 10 and 20m bands
    """
    refb = inputs.refb
    refg = inputs.refg
    refr = inputs.refr
    refre = inputs.refre
    refnir = inputs.refnir

    outputs.outimg = numpy.vstack((refb, refg, refr, refre, refnir))


def copyScaling(cmdargs):
    """
    Set layer names.
    """

    # Set explicit layer names 1 to 5
    layerNames = ['B1', 'B2', 'B3', 'B4', 'B5']
    ds = gdal.Open(cmdargs.outfile, gdal.GA_Update)
    for i in range(5):
        band = ds.GetRasterBand(i + 1)
        band.SetDescription(layerNames[i])

    del ds


if __name__ == "__main__":
    mainRoutine()