#!/usr/env/python3
"""
Author: Cove Technology, Ryan Summers

Description: Provide pyserial-like comport listings with corrections for windows.
"""
import os

# Implement a custom fix for USB composite device serial number identification on windows.
if os.name == 'nt':
    import autotest.tools.list_ports_windows as list_ports
else:
    import serial.tools.list_ports as list_ports


def comports(vid=None, pid=None):
    """ Provide port information filted by product and vendor ID.

    Args:
        vid: An optional vendor ID to search for. If None, vendor ID is not checked.
        pid: An optional product ID to search for. If None, product ID is not checked.

    Returns:
        A list of `pyserial.ListPortInfo` objects with matching VID and PID.
    """
    all_info = list_ports.comports()
    matching_info = []
    for info in all_info:
        vid_match = not vid or vid == info.vid
        pid_match = not pid or pid == info.pid
        if vid_match and pid_match:
            matching_info.append(info)

    return matching_info
