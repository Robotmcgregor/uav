#!/usr/bin/env python
"""
this script applys the dji classifer to a list of dji (UAV) imagery 
Author: Grant Staben
Date: 16/07/2019
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

    p = argparse.ArgumentParser()

    p.add_argument("-s","--imglist", help="provide the path and name of the csv file with the list of imagery to process")
    
    p.add_argument("-d","--direc", help="path to the directory containing the imagery")
    
    p.add_argument("-c","--csv", help="provide the path to the directory and name of the csv file containing the results")
    
    cmdargs = p.parse_args()
    
    # if there is no image list the script will terminate
    if cmdargs.imglist is None:

        p.print_help()

        sys.exit()

    return cmdargs


def applyModel(imglist,directory):
    
    """
    produce the classified image from a image chip representing a site 
    and extract out the total fpc value for the plot. 
    Save the image chip and save out the fpc results as a csv file
    """
    
    site_list = []
    fpc_value_list = []
    fpc_C_value_list = []
    fpc_S_value_list = []
    
    # open the list of imagery and read it into memory
    df = pd.read_csv(imglist,header=None)
    
    for index, row in df.iterrows():
        dji_image = directory + (str(row[0]))
        
        fileN = (str(row[0]))
        
        outfile = directory + fileN[:-4] + '_dji_class.tif'
        
        #print (fileN)
        #print (outfile)         
 
        # call and run the vegetation index scripts
        # to get this to work on windows the code being called by os.system needs to be stored 
        # and run from the same directory. 
    
        cmd = "python PP_C_DJI_Model_V2.py --reffile %s --outfile %s"% (dji_image,outfile) 
        #subprocess.call(cmd, shell=True)    
        os.system(cmd)
        print (outfile + ' complete')
        
        # read in the classified image and calculate the estimated fpc
        # read in with rasterio
        dataset = rasterio.open(outfile)
        # read in the first band as numpy array
        band1 = dataset.read(1)
        
        # get the shape of the image chip which to calculate the percentage fpc
        numPixels = (band1.shape[0] * band1.shape[1])
        
        # get the number of pixels classifed as green mangroves and calculate the % FPC for the site 
        greenM = band1[band1 <= 2]
        greenMc = (greenM.shape[0])
        
        greenC = band1[band1 == 10]        
        greenCc = (greenC.shape[0]) 
        
        greenS = band1[band1 == 11]        
        greenSc = (greenS.shape[0])        
        
        fpc = (greenMc / numPixels)*100
        fpcC = (greenCc / numPixels)*100
        fpcS = (greenSc / numPixels)*100
        
        site_list.append(fileN)
        
        fpc_value_list.append(fpc)
        
        fpc_C_value_list.append(fpcC)
        
        fpc_S_value_list.append(fpcS)
        
    return (site_list, fpc_value_list, fpc_C_value_list, fpc_S_value_list)  
           
# calls in the command arguments and applyModel function.        
def mainRoutine():
    
    cmdargs = getCmdargs()
    directory = str(cmdargs.direc)
    csvfile = str(cmdargs.csv)
    
    site_list, fpc_value_list, fpc_C_value_list, fpc_S_value_list = applyModel(cmdargs.imglist,directory)

    # save out the results to a csv file
    data = list(zip(site_list, fpc_value_list, fpc_C_value_list, fpc_S_value_list))
    
    results = pd.DataFrame(data,columns=['site','PVm', 'PVc', 'PVs'])
           
    results.to_csv(csvfile)
    
    
if __name__ == "__main__":
    mainRoutine()
    