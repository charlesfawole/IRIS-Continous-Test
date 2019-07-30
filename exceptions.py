#!/usr/bin/python3
"""
Author: Cove Technology, Ryan Summers

Description: Provides definitions for exceptions within the AutoTest package.
"""

class AutoTestException(Exception):
    """ Base class exception for all AutoTest package exceptions. """


class ResourceNotFound(AutoTestException):
    """ Basic exception when a resource is not available. """

    
class WandCommException(Exception):
    def __init__(self,message="WandComm Error",code=-1):
        
        super().__init__(message)
        self.message = message
        self.code = code
    def getMessage(self):
        return self.message
    def getCode(self):
        return self.code
        
        
class DevKitConnectionException(Exception):
    def __init__(self,message="Dev Kit Error",code=-1):
        super().__init__(message)
        self.message = message
        self.code = code
    def getMessage(self):
        return self.message
    def getCode(self):
        return self.code