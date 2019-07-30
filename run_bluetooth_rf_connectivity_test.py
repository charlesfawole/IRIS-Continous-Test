"""
Author: Cove Technology, Ryan Summers

Description: Runs an automated bluetooth connectivity test for the Sentiva 2.0 project.
"""
import argparse
import json
import logging
import os
import random
import sys

#from autotest.framework.test_results import TestResults
#from autotest.framework.hardware_manager import HardwareManager
#from autotest.framework.timer import RealTimer

from bluetooth_rf_connectivity_test import BluetoothConnectivityTest

from MSP_FW_Loader import MSP_FW_Loader
from FW_From_SVN import FW_From_SVN
from Nordic_FW_Loader import Nordic_FW_Loader

def main():

    #test = BluetoothConnectivityTest()
    #while True:
    #    test.connection_callback('0','0')
        # Construct the test and run it.
       
    latestRevisionNumber='0'
    latestBuildNumber    = '0'
    
    test = BluetoothConnectivityTest()
        
    fw_svn = FW_From_SVN()
    mspFW_loader = MSP_FW_Loader()
    nordicLoader = Nordic_FW_Loader()
    
    fw_svn.getTopOfTrunkFW()
    latestBuildNumber = fw_svn.getLatestFWBuildNumber()
    latestRevisionNumber = fw_svn.getLatestRevisionNumber()
    
    print(latestRevisionNumber)

    mspFW_loader.programMSP(latestBuildNumber)
    nordicLoader.programNordic(NordicFWFolder=latestBuildNumber)
    
    
    error_msg = ""
    while True:
        if (latestBuildNumber != fw_svn.getLatestFWBuildNumber()):
            try:
                print("loaded firmware is not latest from SVN")
                print ("\r\n\r\n")
                fw_svn.getTopOfTrunkFW()
                latestBuildNumber = fw_svn.getLatestFWBuildNumber()
                latestRevisionNumber = fw_svn.getLatestRevisionNumber()
                mspFW_loader.programMSP(latestBuildNumber)
                nordicLoader.programNordic(NordicFWFolder=latestBuildNumber)
                error_msg = "No errors"
            except Exception:
                error_msg = "firmwareload error"
                print ("FW load exception")
                #raise Exception("FW Load")
    
        else:
            try:
                test.connection_callback(latestRevisionNumber,latestBuildNumber,error_msg)
            except Exception as ex:
                #raise Exception
                print (ex)
        

main()
