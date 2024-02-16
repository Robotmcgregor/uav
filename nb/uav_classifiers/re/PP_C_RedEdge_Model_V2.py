#!/usr/bin/env python


"""
This code uses the sklearn 0.21.3 version.


Definition              Class

Dark green               1
Light green              2
Dark npv                 3
Light npv                4
Dark shadow              5
Light shadow             6
Dark bare ground         7
Light bare ground        8
Rocks                    9
Chenopod                10
Seagrass                11
Water                   12

"""

from __future__ import print_function, division
import sys
import os
import argparse
import pickle as pickle
import numpy as np
from rios import applier, fileinfo
import pdb
from sklearn.preprocessing import Imputer

def getCmdargs():
    """
    Get command line arguments
    """
    p = argparse.ArgumentParser()
    p.add_argument("--reffile", help="Input the image")
    
    p.add_argument("--outfile", help="Name of output file")
    
    p.add_argument("--picklefile", default="rfc_cpickle_re_20220426.p",help="Input pickle file (default is %(default)s)")
    
    cmdargs = p.parse_args()
    
    if cmdargs.reffile is None:
        p.print_help()
        sys.exit()
        
    return cmdargs


def main():
    """
    Main routine
    
    """
    cmdargs = getCmdargs()
    controls = applier.ApplierControls()
    infiles = applier.FilenameAssociations()
    outfiles = applier.FilenameAssociations()
    otherargs = applier.OtherInputs()
    
    infiles.image = cmdargs.reffile
    
    imageExt = infiles.image
         
    controls.setReferenceImage(infiles.image) 
    
    outfiles.hgt = cmdargs.outfile
    
    otherargs.rf = pickle.load(open(cmdargs.picklefile, 'rb'))
    # refInfo = fileinfo.ImageInfo(infiles.sfcref)

    otherargs.refnull =  -10000

    applier.apply(doModel, infiles, outfiles, otherargs,controls=controls)
    
    
    
def doModel(info, inputs, outputs, otherargs):

    nonNullmask = (inputs.image[0] != otherargs.refnull)
    
    # get the shape of the annual image and convert it to the shape of a single band  
    imgshape = inputs.image.shape
    # convert the tuple to a list to convert all bands to represent 1 band and then convert it back to a tuple
    list_imgshape = list(imgshape)
    list_imgshape[0] = 1
    imgShape = tuple(list_imgshape)

    # input the predictor variables 
    
    blue = (inputs.image[0][nonNullmask]).astype(np.float32)
    green = (inputs.image[1][nonNullmask]).astype(np.float32)
    red = (inputs.image[2][nonNullmask]).astype(np.float32)
    nir = (inputs.image[3][nonNullmask]).astype(np.float32)
    rededge = (inputs.image[4][nonNullmask]).astype(np.float32)

    
        
    # pass the variables into a np array and transform it to look like the pandas df 
    
    allVars= np.vstack([blue, green, red, nir, rededge,]).T
        

   
    # sets up the shape and dtype for the chm output  
    outputs.hgt = np.zeros(imgShape, dtype=np.uint8)
    
    # applies the rfr model to produce the chm layer
    
    if allVars.shape[0] > 0:
        # run check over the input data and replaces nan and infinity values
        allVars[np.isnan(allVars)] = 0.0
        allVars[np.isinf(allVars)] = 0.0
        
        hgt = otherargs.rf.predict(allVars)
        
        outputs.hgt[0][nonNullmask] = hgt
    

if __name__ == "__main__":
    main()
