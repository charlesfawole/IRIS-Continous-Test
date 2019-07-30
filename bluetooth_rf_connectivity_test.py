#!/usr/env/python3
"""
Author: Cove Technology, Ryan Summers

Description: A hardware test to exercise bluetooth connectivity of the Sentiva 2.0 device.
"""

import time,datetime,random


from  sentiva_monitor import SentivaMonitor
from sentiva_wand import SentivaWand

#from autotest.framework.hardware_test import HardwareTest
#from autotest.framework.rules import ConstantValueRule, MinimumValueRule

from exceptions import ResourceNotFound, AutoTestException,WandCommException,DevKitConnectionException




class ConnectionException(AutoTestException):
    """ Custom exception for issues relating to BLE connections. """


class BluetoothConnectivityTest():
    """ An automated hardware test to verify Bluetooth RF connectivity of the Sentiva 2.0
        implant.
    """

    # The RSSI used when no valid RSSI can be reported.
    WORST_RSSI = -150.0

    EXPECTED_BLUETOOTH_NAME = "IPG_EA271A"
    MIN_EXPECTED_RSSI = -85.0
    SCAN_DURATION = 1
    NUM_RSSI_SAMPLES = 10
    MAX_SCAN_ATTEMPTS = 600  # 10 minutes timeout for scan and connect
    ADV_INTERVAL = 1


    logFile = open("RSSILog_root_cause_test_svn_fw5.csv","w+")
    logFileRemote = open("C:\\Users\\charles.fawole\\Box Sync\\RF IPG\\M1100 Jenkins\\Test Plan for BLE Discovery\\svn_fw5.csv","w+")
    #logFile.write('Index,TimeStamp, Test Time Total (s), Number of Attempts, BLE Name, ScanSucess, Scan Latency(s), ConnectionSuccess, Connection Latency (s), advertising interval (s), scanInterval (ms), scanWindow (ms), IntervalAndWindow(ms:ms) \n')
    #logFileRemote.write('Index,TimeStamp, Test Time Total (s), Number of Attempts, BLE Name, ScanSucess, Scan Latency(s), ConnectionSuccess, Connection Latency (s), advertising interval (s), scanInterval (ms), scanWindow (ms), IntervalAndWindow(ms:ms) \n')
		
    
    

    def __init__(self):

        self.implant_monitor = SentivaMonitor('COM8','000683808454',None)
        self.wand = SentivaWand()
                
        self.connection_attempt_number = 0
        self.connection_holdoff_duration = 0
  
    def record_measurement(self,ind='0',Tstamp=datetime.datetime.now(),
                            Telapsed='0',
                            Nattempt='0',
                            Bid='0',
                            Bscan='False',
                            Tscan='0',
                            Bconn='False',
                            Tconn='0',
                            AdvInterval='0',
                            ScanInterval='0',
                            ScanWindow ='0',                            
                            IntervalAndWindow='0:0',
                            svn_rev = '0',
                            fw_build = '0',
                            msp_ver = '0',
                            nordic_ver = '0',
                            error_msg=' No err',
                            avg_rssi='0',
                            ):
        
        self.logFile.write(ind+Tstamp+Telapsed+Nattempt+Bid+Bscan+Tscan+Bconn+Tconn+AdvInterval+ScanInterval+ScanWindow+IntervalAndWindow+svn_rev+fw_build+msp_ver+nordic_ver+error_msg+avg_rssi+'\n'  )
        self.logFile.flush()
        self.logFileRemote.write(ind+Tstamp+Telapsed+Nattempt+Bid+Bscan+Tscan+Bconn+Tconn+AdvInterval+ScanInterval+ScanWindow+IntervalAndWindow+svn_rev+fw_build+msp_ver+nordic_ver+error_msg+avg_rssi+'\n'  )
        self.logFileRemote.flush()
    def connection_callback(self, svn_n,fw_build,error_msg):
        
        
        scanParamStep = 10
        minScanParam = 60
        maxScanInterval = 1000
        minAdvInterval = 1
        advIntervalStep = 1
        maxAdvInterval = 5
        
        Nrep = 1
        
        
        #scanIntervals = range(minScanParam,maxScanInterval+scanParamStep,scanParamStep)    # scan intervals
        scanIntervals = [40] #range(minScanParam,maxScanInterval,scanParamStep)    # scan intervals
        advIntervals = [1]#[500,1500,2500,3500,4500]#[760.0,546.25,417.5,318.75,211.25,152.5,20]# [1285.0,1022.5,852.5, range(minAdvInterval,maxAdvInterval+advIntervalStep,advIntervalStep)          # advertising intervals
        #advIntervals = [a/1000.0 for a in advIntervals]        

        reps = range(Nrep)   # number of times to repeat each combination of factors
        
        v_msp = '0'
        v_nordic = '0'
        
        
        
        for scanInterval in scanIntervals:
            scanWindows = [30]#range(10,scanInterval+scanParamStep,scanParamStep)
            for scanWindow in scanWindows:
                for advInterval in advIntervals:
                    
                    
                    
                    
                    try:
                        self.wand.enable()
                        print (self.wand._execute_command('setserial(15345434)'))
                        self.wand.enable_device_bluetooth(advInterval) # turn on bluetooth at set advertising interval to 1 seconds
                        #print("about to set millisec inter")
                        #self.wand.set_InMilliSecondInterval(advInterval)
                    except Exception:
                        time.sleep(2)
                        self.wand.enable()
                        self.wand._execute_command('setserial(15345434)')
                        self.wand.enable_device_bluetooth(advInterval) # turn on bluetooth at set advertising interval
                        #print("about to set millisec inter")
                        #self.wand.set_InMilliSecondInterval(advInterval)
                        
                    
                    for index in reps:
                        exception_msg = error_msg
                        test_time=0
                        implant_bluetooth_id=" "
                        implant_detected = " "
                        scan_duration_seconds = 0 
                        implant_connected = " "
                        connection_duration_seconds = 0
                        setScanParams = [0,0]
                        advInterval = 0
                        v_msp ='0' 
                        v_nordic='0'
                        rssi = self.__class__.WORST_RSSI
                         
                        
                        
                        test_time_start = time.time()
                        try:
                            print('Run Number {}'.format(index))
                            print('Advertising Interval {}'.format(advInterval))
                            print('Scan Interval {}'.format(scanInterval))
                            print('Scan Window {}'.format(scanWindow))
                            
                            
                            
                            time.sleep(random.random()*advInterval)  # muddle things up, make things less deterministic by begining to scan a random time after
                        
            
            
            
                            """ Attempt to connect to the implant over bluetooth. """
                            self.connection_attempt_number += 1
    
                            print('Bluetooth connection attempt {}'.format(self.connection_attempt_number))
    
                            
                            self.wand.enable()
    
                            (_, version) = self.wand.get_ipg_version()
    
                            print('IPG Version: {}'.format(version))
                            
                                                        
                            v_msp = self.wand._execute_command('v')
                            v_nordic = self.wand._execute_command('readx 13 4 2')
                           
    
                            #enable ble device at the specified advertising interval
            
                            #self.equipment.wand.enable_device_bluetooth(self.__class__.ADV_INTERVAL)
    
                            # Reset the implant monitor and scan for the implant.
                            
                            
    
                            implant_detected = False
                            implant_connected = False
                            scan_duration_seconds = -1
                            implant_bluetooth_id = 'Unknown'
                            num_bluetooth_devices_detected = 0
                            connection_duration_seconds = -1
                            rssi = self.__class__.WORST_RSSI
    
                            time.sleep(1.0)

                            #Reset the monitor at the beginning of each test
                            self.implant_monitor.reset()
                            setScanParams = self.implant_monitor.setScanParams(scanInterval,scanWindow)
                
                            # Scan for the device.
                            scan_start_time = time.time() #self.timer.get_time()
                
                            all_detected_devices = []
                            for attempt in range(0, self.__class__.MAX_SCAN_ATTEMPTS):
                                print("{}/{} Scanning for device".format(attempt+1, self.__class__.MAX_SCAN_ATTEMPTS))
                                all_detected_devices += self.implant_monitor.ble_scan(
                                    self.__class__.SCAN_DURATION)
                
                                implant_detected = self.__class__.EXPECTED_BLUETOOTH_NAME in \
                                                   [x.name for x in all_detected_devices]
                
                                if implant_detected:
                                    scan_duration_seconds = time.time() - scan_start_time
                                    break
                
                            
                
                            detected_devices = set(all_detected_devices)
                            num_bluetooth_devices_detected = len(detected_devices)
                            #display all discovered devices
                            for device in detected_devices:
                                print("SCAN: Found Device named {}".format(device.name))
                            # If the device was not found in the scan, abort out now - we can't connect.
                            if implant_detected is False:
                                scan_duration_seconds = time.time() - scan_start_time
                                raise DevKitConnectionException('Device not found during bluetooth scan',-1)
                
                            for device in detected_devices:
                                if device.name == self.__class__.EXPECTED_BLUETOOTH_NAME:
                                    implant_bluetooth_id = device.identifier
                                    break
                
                            # Connect to the bluetooth device.
                            time.sleep(random.random()*advInterval)  # muddle things up, make things less deterministic by begining to connect a random time after
                            connection_start_time = time.time()
                            
                            print("Attempting to connect to Device")

                            try:
                                self.implant_monitor.ble_connect(
                                    
                                        self.__class__.EXPECTED_BLUETOOTH_NAME,self.__class__.MAX_SCAN_ATTEMPTS)  # set same timeout for connect as for scan
                                implant_connected = True
                                print("Connected to Implant")
                            except Exception:
                                connection_duration_seconds = time.time() - connection_start_time
                                implant_connected = False
                                raise DevKitConnectionException('Failed to connect to IPG over BLE',-1)
                
                            
                            
                
                            connection_duration_seconds = time.time() - connection_start_time
                            print('Scan Latency {} s'.format(connection_duration_seconds))
                            print('Connection Latency {} s'.format(scan_duration_seconds))
                
                            # Finally, get the RSSI of the connection.
                            rssi_accumulator = []
                            for x in range(self.__class__.NUM_RSSI_SAMPLES):
                                attempt = "{}/{}".format(x+1, self.__class__.NUM_RSSI_SAMPLES)
                                try:
                                    rssi = self.implant_monitor.ble_rssi()
                                    print("{} RSSI: {} dBm".format(attempt, rssi))
                                    rssi_accumulator.append(rssi)
                                except Exception as ex:
                                    #trap the exception thrown with the RSSI measurement doesn't return
                                    print("{} RSSI: Failed to return".format(attempt))
                                    raise DevKitConnectionException("RSSI Connection Exception")
                
                           
                
                            if rssi_accumulator:
                                rssi = float(sum(rssi_accumulator) / len(rssi_accumulator))
                                print('Connection successful. RSSI: {} dBm'.format(rssi))
                            

                            test_time= time.time() - test_time_start


                
                        except Exception as e:
                            #raise Exception
                            print("there was an exception??     "+e.message)
                            exception_msg = e.message
                            raise Exception
                        finally:
                            self.record_measurement(ind = str(index)+',',Tstamp = str(datetime.datetime.now())+',',
                            Telapsed=str(test_time)+',',
                            Nattempt=str(self.connection_attempt_number)+',',
                            Bid=str(implant_bluetooth_id)+',',
                            Bscan=str(implant_detected)+',',
                            Tscan=str(scan_duration_seconds)+',',
                            Bconn=str(implant_connected)+',',
                            Tconn=str(connection_duration_seconds)+',',
                            AdvInterval=str(advInterval)+',',
                            ScanInterval=str(setScanParams[0])+',',
                            ScanWindow =str(setScanParams[1])+',',                            
                            IntervalAndWindow=str(setScanParams[0])+':'+str(setScanParams[1])+',',
                            svn_rev = str(svn_n)+',',
                            fw_build = fw_build+',',
                            msp_ver = v_msp+',',
                            nordic_ver =  v_nordic+',',
                            error_msg = exception_msg+',',
                            avg_rssi=str(rssi)+',',
                            )
                        

                        
                        # Disconnect from the implant bluetooth connection.
                        self.implant_monitor.ble_disconnect()
                
                    # Disable bluetooth on the implant.
                    self.wand.enable()
                    self.wand.disable_device_bluetooth()
                            
        #self.logFile.close()
        #self.logFileRemote.close()
        return 0            