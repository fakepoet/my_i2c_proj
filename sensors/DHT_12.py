# coding: utf-8


import smbus

DEVICE_ADDR = 0x5C  # device address
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1


class DHT12(object):
    def __init__(self, addr=DEVICE_ADDR):
        self.addr = addr

    def read_data(self):
        # read 5 bytes of data from the device address (0x05C) starting from an offset of zero
        data = bus.read_i2c_block_data(self.addr, 0x00, 5)

        humidity = "{}.{}%".format(str(data[0]), str(data[1]))
        temp = "{}.{}{}C".format(data[2], data[3], chr(0xDF))

        if (data[0] + data[1] + data[2] + data[3] == data[4]):
            return True, (humidity, temp)
        else:
            return False, 'DHT12 ERROR:\n' + 'CHECK FAILED.'.rjust(16)


dht_12 = DHT12()
