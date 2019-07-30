"""
Author: Cove Technology, Ryan Summers

Description: Driver for the Nordic breakout board that communicates with the Sentiva 2.0 implant.
"""

import re
import time

import recordclass
import serial


from exceptions import DevKitConnectionException
#from serial_util import serial_util


class SentivaMonitor():
    """ Control and monitor a Sentiva 2.0 implant. """

    USB_VID = int('1366', 16)
    USB_PID = int('1015', 16)

    ScannedDevice = recordclass.recordclass('ScannedDevice', ['name', 'identifier', 'index'])

    ScannedDevice.__hash__ = lambda x: hash((x.name, x.identifier, x.index))


    def __init__(self, name, serial_number=None, device_filter=None):
        """ Initialize a USB serial device.

        Args:
            name: The name of the equipment.
            serial_number: The USB device serial number of the desired equipment. If not supplied,
                the driver will attempt to instantiate a device if only one is available.
            device_filter: A function that will be provided the `serial.ListPortInfo` objects
                detected with the respective VID/PID that shall return True if the device should be
                considered further. This is typically a lambda function.

        Note:
            This function searches available USB COM ports for the specified VID, PID, and serial
            number pairing.
        """
        self.port_name = name
        self.port = serial.Serial(self.port_name, baudrate=115200)
        self.scanned_devices = []


    def shutdown(self):
        """ Shutdown the monitor. """
        self.disable()


    def reset(self):
        """ Reset the monitor. """
        self.ble_disconnect()
        self._execute_command('reboot')


    def is_enabled(self):
        """ The monitor is always enabled. """
        return True


    def disable(self):
        """ The monitor is always enabled. """


    def enable(self):
        """ The monitor is always enabled. """


    def _execute_command(self, command, arg=None, timeout=0.5):
        """ Execute a command on the monitor.

        Args:
            command: The command to execute.
            arg: An optional argument to provide to the command to execute.
            timeout: The duration to wait for the command to complete in seconds.

        Returns:
            The text output of the command.
        """
        command_string = '{}({})\r\n'.format(command, arg if arg else '')

        self.port.reset_input_buffer()
        self.port.write(command_string.encode('ascii'))
        time.sleep(timeout)

        return self.port.read(self.port.inWaiting()).decode('ascii')

    def _poll_for_response(self, interval, num_checks):
        """ Poll the monitor for a response. Some commands have a non-deterministic and long response time

        Args:
            interval: The time (seconds) to wait before checking for a response
            num_checks: The number of times to check
        """
        for _ in range(num_checks):
            resp = self.port.read(self.port.inWaiting()).decode('ascii')
            if resp:
                return resp
            else:
                time.sleep(interval)
        return ""

    def ble_connect(self, name, timeout=80):
        """ Connect the monitor to a bluetooth device. Wait for the connected
            message from the Nordic Dev Kit
            
        Notes:
            The name must be previously detected in a bluetooth scan.

        Args:
            name: The bluetooth name of the intended peer.
            timeout: The length of time to wait for a connect message

        """

        device_index = None
        for device in self.scanned_devices:
            if name == device.name:
                device_index = device.index

        if not device_index:
            raise DevKitConnectionException('Attempting to connect to a device that was not scanned.',-1)

        self._execute_command('connect', device_index)
        
        #The SDK returns "Connection complete"
        resp = self._poll_for_response(1, timeout)
        if "complete" not in resp:
            #Raise the exception that the expected device wasn't found
            raise DevKitConnectionException("Could not Connect over BLE")

    def ble_scan(self, duration):
        """ Scan for BLE peripheral devices.

        Args:
            duration: The duration to perform the scan (in seconds)

        Returns:
            A list of ScannedDevice objects.
        """
        self.scanned_devices.clear()
        self._execute_command('scan')

        time.sleep(duration)

        output = self._execute_command('list')

        if not output:
            return

        for entry in output.split('\n'):
            match = re.match(r'^\[(\d+)\]:: (\S+)  \"(.*)\".*', entry)
            if not match:
                continue

            self.scanned_devices.append(self.__class__.ScannedDevice(name=match.group(3),
                                                                     identifier=match.group(2),
                                                                     index=match.group(1)))

        return self.scanned_devices


    def ble_disconnect(self):
        """ Disconnect from a connected BLE device. """
        self._execute_command('disconnect')


    def ble_rssi(self):
        """ Get the RSSI of the BLE connection.

        Returns:
            The received signal strength indicator in dBm.
        """
        #TODO: This is an unstable measurement. The call to this function
        #is wrapped with a try/except in the event that no RSSI data is returned.

        #The RSSI takes ?? seconds to happen, set timout to ensure that
        #at least 1 RSSI measurement takes place
        output = self._execute_command('startRSSI', timeout=2)
        self._execute_command('stopRSSI', timeout=0.1)

        rssi = re.search('Rssi is (-?\d+) with conn_handle', output)
        if not rssi:
            raise Exception('No RSSI detected. Is the device connected?')

        return int(rssi.group(1))
    
    
    def setScanParams(self,interval,window):
        """set the scan paramters of the Dev Kit. Interval is scan Interval in ms, and window is scan window in ms
        
        Returns:
            The set parameters
            
        """
        
        res = self._execute_command("cscani",interval)
        res=res+self._execute_command("cscanw",window)
        res = res.split()
        setInterval = (int)(int(res[6])*0.625)   # the firmware return in unit of 0.625 millisecodns
        setWindow = (int)(int(res[14])*0.625)
        return [setInterval, setWindow]