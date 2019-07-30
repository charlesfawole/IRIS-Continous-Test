import subprocess
import os



class MSP_FW_Loader():


   def programMSP(self,MSPfirmwareFolder):

       MSPfirmwareFolder = "C:\\Users\\charles.fawole\\Box Sync\\RF IPG\M1100 Firmware Builds\\"+MSPfirmwareFolder+"\\"
       firmwareFile = MSPfirmwareFolder+"msp_therapy_and_bootloader.hex"


       
       print("FIRMWARE FILE IS : "+firmwareFile)
       print("loading MSP Firmware...")
       
       #p = subprocess.Popen(["MSP430Flasher.exe", '-w', firmwareFile, "-v", "-g", "-z", "[VCC]"], stdout=subprocess.PIPE)
       #out, err = p.communicate()

       #out = str(out)

       ##print (out)
       #if "No error" in out:
       #    print("no error with MSP FW load")
       #else:
       #     raise Exception("error with MSP FW load!")
       
       subprocess.run(["MSP430Flasher.exe", '-w', firmwareFile, "-v", "-g", "-z", "[VCC]"])
    



