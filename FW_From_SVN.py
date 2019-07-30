import subprocess
import os

class FW_From_SVN():


    def getTopOfTrunkFW(self):
        os.chdir("C:\\Users\\charles.fawole\\Box Sync\\RF IPG\\M1100 Firmware Builds\\")
        subprocess.run(["C:\\Users\charles.fawole\\Box Sync\\RF IPG\\M1100 Firmware Builds\\automated_firmware_download.cmd"])
        os.chdir(".")

    def getLatestRevisionNumber(self):   # use the build number file to determine this
       
        
        p = subprocess.Popen(["C:\\Users\\charles.fawole\\Box Sync\\RF IPG\\M1100 Firmware Builds\\getTopRevNumber.cmd"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        a = str(out)
        signature = "Last Changed Rev:"   # or "Revision:"
        start = a.find(signature)+len(signature)
        end = a.find("\\r",start)
        revisionNumber = a[start:end]
        
        print ("revison number {}".format(revisionNumber))

        return int(revisionNumber)

    def getLatestFWBuildNumber(self):
        os.chdir("C:\\Users\\charles.fawole\\Box Sync\\RF IPG\\M1100 Firmware Builds\\")
        p = subprocess.Popen(["svn", "--username", "cfawole", "--force", "export", "https://polarion.cyberonics.com/repo/PDP Projects/Neuromodulation System Projects/SenTiva 2.0 Bluetooth/code/trunk/applications/build_number.h", "."],stdout=subprocess.PIPE)
        out, err = p.communicate()
        a = str(out)
        with open('build_number.h', 'r') as f:

            first_line = f.readline()
        print (first_line)
        return first_line[:-1] # do not return the end of line character