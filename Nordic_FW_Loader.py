import subprocess
import os

class Nordic_FW_Loader():
    
    def programNordic(self, NordicFWFolder,serialNumber = "683772875"):

        "C:\\Users\\charles.fawole\\Box Sync\\RF IPG\M1100 Firmware Builds\\"+NordicFWFolder+"\\"
        os.chdir(NordicFWFolder)
        subprocess.run(["nrfjprog","-s",serialNumber,"-e"])
        subprocess.run(["nrfjprog","-s",serialNumber,"--program", "softdevice.hex"])
        subprocess.run(["nrfjprog","-s",serialNumber,"--program", "arm_bootloader.hex"])
        subprocess.run(["nrfjprog","-s",serialNumber,"--program", "arm_server.hex"])
        subprocess.run(["nrfjprog","-s",serialNumber,"--debugreset"])
        os.chdir(".")
        
