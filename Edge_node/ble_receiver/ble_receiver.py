import os
from bluepy import btle
from binascii import hexlify
import time, uuid, json, requests
from logger import Logger


# Definitions 
SERVICE_UUID   = uuid.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
WRITE_CHR_UUID = uuid.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')
NOTIFY_CHR_UUID = uuid.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')
TARGET_NAME  = 'MZB24C20R(A)'
device_list = []
log = Logger("BLE")


# API 
api_user        = "admin"
api_password    = "uched4123"
base_url        = "http://127.0.0.1:8002/"
request_headers = {'Content-Type': 'application/json',}

test_device_id      = "7E528A676931"
test_device_type    = "RR"


def api_send_data(self, device_id, value, device_type):
    data = {
        "device_id": device_id,
        "time": int(time.time()),
        "value" : value
    }
    url = base_url + "sensordata/" + device_type + '/'
    r = requests.post(url, headers=request_headers, auth=(api_user, api_password), data=json.dumps(data))

     
class ScanDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        return
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

class DeviceDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        #print(len(data))
        if data[16] == 0xA7:
            val = (data[17] << 8) | data[18]
            print(f"RR: {val}")
        #print("Received data %s " % hexlify(data))



if __name__ == "__main__":
    log.debug("Starting BLE Receiver")
    scanner = btle.Scanner().withDelegate(ScanDelegate())

    while True:
        devices = scanner.scan(5.0, passive=True)
        for dev in devices:
            try:
                dev_data = dev.getScanData()
                dev_name = dev_data[1][2] or None

                if dev_name == TARGET_NAME:
                    log.debug("Found Mezoo Device")
                    log.debug(f"Connecting to: {dev.addr}")
                
                    periph = btle.Peripheral(dev, "random")     # supply scan entry as arg
                    periph.setDelegate(DeviceDelegate())

                    # Setup to turn notifications on
                    svc = periph.getServiceByUUID(SERVICE_UUID)
                    ch = svc.getCharacteristics(NOTIFY_CHR_UUID)[0]
                    print("ch", ch)
                    periph.writeCharacteristic(ch.getHandle()+1, b"\x01\x00", True)

                    while True:
                        if periph.waitForNotifications(1.0):
                            continue

            except Exception as e:
                pass
                #print(e)

        time.sleep(2)

'''
# Main loop --------

# Initialisation  -------

p = btle.Peripheral( device_address, "random" )
p.setDelegate( MyDelegate() )
p.setMTU(230)

setup_data = bytearray([read_flash_page_command, 1, 1])

# Setup to turn notifications on, e.g.
svc = p.getServiceByUUID( SERVICE_UUID )
ch = svc.getCharacteristics( CHAR_UUID )[0]

# Descriptor update to CCCD and enable notification 
p.writeCharacteristic(ch.getHandle()+1, b"\x01\x00", True)

ch.write( setup_data )

while True:
    if p.waitForNotifications(1.0):
        # handleNotification() was called
        continue

    print ("Waiting...")
    # Perhaps do something else here

	
	
'''