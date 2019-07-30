"""
Author: Cove Technology, Ryan Summers

Description: Driver for the Sentiva 2.0 wand to control the implant.

Uses Fcall Commands to communicate with the wand through a C# wrapper class. 
Complete fcall documentation in ipg interface document. Summary below

FCALL 0 0x115 <on> Controls the BLE radio. Legal values for "on" are 0 - 2.
 The value of "on" is stored in trims value "blestate" and persists through IPG reboots.
 on:
     0: Turn BLE radio off, put Nordic co-processor into deepsleep mode.

     1: Wake Nordic co-processor, turn BLE radio on, and start BLE advertising
         at high power for "rto" seconds. If no BLE connection is made within
         "rto" seconds the BLE radio is turned off and the Nordic co-processor
         is put into deepsleep mode.

     2: Wake Nordic co-processor, turn BLE radio on, and start BLE advertising
         at "cd" power indefinitely.
         
         
 FCALL 0 0x116 <cd> <rts> <rto> <ai>
 
     Dynamically updates BLE radio parameters and saves to trims. These
     values persist through reboot. Parmeters defined below:

     cd: Represents the communications distance of the BLE radio:
             0: ................ -40 dB
             1: short range .... -20 dB
             2: ................ -16 dB
             3: ................ -12 dB
             4: ................ -8 dB
             5: ................ -4 dB
             6: medium range ... 0 dB
             7: ................ 3 dB
             8: long range ..... 4 dB

         range: 0 - 255, value saturates at 8 (i.e., >8 -> 8)

     rts: The time in minutes when the BLE radio will transition to short range (-20 dB).
         While the BLE radio is advertising and no connection is made within rts minutes,
         the IPG will transition to short range.
         While the BLE radio is connected and no TLV packets are transmitted/received for
         rts minutes, the IPG will transtion to short range.

         range: 0 - 255 (minutes)

     rto: The time in seconds the IPG will allow the BLE to remain temporarily
         advertising. (See radio_on()) If the IPG does not make a BLE connection,
         or the IPG is not told to transition to permenant advertising, after
         rto seconds the IPG will stop BLE advertising, turn off the BLE radio
         and put the Nordic co-processor into deep sleep mode.

         range: 0 - 255 (seconds)

     ai: The advertising interval
         range: 0 - 15 (seconds), upper 4 bits are ignored

"""

import os
import sys
from exceptions import WandCommException

#from autotest.equipment import TestEquipment
#from autotest.exceptions import AutoTestException

# Import the custom TivaComm .NET DLL as a python module.
try:
    import clr
    sys.path.append(os.path.join(os.path.dirname(__file__), 'dll\\'))
    clr.AddReference('TivaComm')
    from TivaComm import WandComm

except:
    raise WandCommException("Error loading WandComm DLL",-1)
    print('Failed to import TivaComm .NET DLL. Please install PythonNet')
    print('SentivaWand driver unavailable.')




class SentivaWand():
    """ Driver class for interacting with the Sentiva 2.0 implant through the wand. """

    def __init__(self):
        
        self.wand = WandComm()
        self.connection_established = False


    def shutdown(self):
        """ Shutdown communications to the wand. """
        self.wand.Stop().Wait()


    def enable(self):
        """ Start communications with the wand. """
        self.wand.Start().Wait()
        self._execute_command('attention')
        self._execute_command('establish')
        self._execute_command('boot')
        self._execute_command('attention')
        self._execute_command('establish')
        self.connection_established = True

        
    def get_ipg_version(self):
        """ Query the IPG for model & version info. """
        #send the 'v' command to return the version
        #return resembles -> Model = 10,  Therapy version = 2.0.0.139
        ret = self._execute_command('v')
        if (len(ret)) == 0:  # if ipg reports no version info, then it must be that Wandcomm is not connected to IPG
            raise WandCommException()
        
        (model, version) = ret.split(',')
        return (model.strip(), version.strip())


    def disable(self):
        """ Stop communications with the wand. """
       # self._execute_command('c') #send the close command
        self.wand.Stop().Wait()
        self.connection_established = False


    def is_enabled(self):
        """ Determine if the wand communication channel is enabled. """
        return self.connection_established


    def reset(self):
        """ There is no way to reset the wand. """
        if self.is_enabled():
            self.disable_device_bluetooth()
        self.disable()


    def _execute_command(self, command):
        response = self.wand.Send(command).Result
        if 'Failed' in response:
            raise WandCommException('Failed to run command {} (Response: {})'.format(command, response),-1)
        # TODO: Examine responses and determine what to do with them.
        return response

    def disable_device_bluetooth(self):
        """ Disable bluetooth on the implant device. """
            
        #FCALL to radio_on = 0x115 with on set to 'off'
        self._execute_command('fcall 0 0x115 0')

    def enable_device_bluetooth(self, advertising_interval):
        """ Enable bluetooth on the implant device.
        TODO: Add power levels, adv duration,
        Args:
            advertising_interval: The time between advertisement packets
        """
        assert advertising_interval < 16 #Valid range is 0-15

        # TODO: Determine the parameters of these magic strings.

        arg_cd  = 1  #Short Range    
        arg_rts = 5  #Minutes until the device transitions to -20dB
        arg_rto = 30 #Seconds to remain in advertising mode - Ignored with radio_on of 2
        arg_ai  = advertising_interval
        fcall = 'fcall 0 0x116 {} {} {} {}'.format(arg_cd, arg_rts, arg_rto, arg_ai)

        # Configure the BLE part on the implant
        self._execute_command(fcall)

        #Turn the radio on to advertise with the settings indefinately
        #TODO remove magic numbers
        self._execute_command('fcall 0 0x115 2')
