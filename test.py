#!/usr/bin/env python3
from rn2483 import Lora
import datetime

# init the serial connection
lora = Lora()

# get device info
lora.get_info_device()

# config the device
lora.config__mac()

# try to join lora gateway
lora.join()


# test to send data
#lora.test_uplink()
time = "".join(str(datetime.datetime.now()).split('.')[0])
lora.send(time)

