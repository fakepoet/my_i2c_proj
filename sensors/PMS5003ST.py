# coding: utf-8
import serial
import time
import struct


class PMS5003(object):

    @staticmethod
    def get_data():
        ser = serial.Serial("/dev/ttyS0", 9600)
        while True:
            sign1 = ser.read()
            print '1: %s' % sign1
            print '1 ord: %s' % ord(sign1)
            if ord(sign1) == 0x42:
                sign2 = ser.read()
                print '2 : %s' % sign2
                print '2 ord: %s' % ord(sign2)
                if ord(sign2) == 0x4d:
                    count = ser.inWaiting()
                    while count < 38:
                        time.sleep(0.2)
                    recv = ser.read(38)
                    (frame_length, pm1_0_cf, pm2_5_cf, pm10_cf, pm1_0,
                     pm2_5, pm10, cnt_03, cnt_05, cnt_10, cnt_25, cnt_50, cnt_100,
                     hcho, temp, humidity, reserve, version, checksum) = struct.unpack('>' + 'H' * 19, recv)
                    ser.close()
                    break
        return dict(
            pm1_0=pm1_0,
            pm2_5=pm2_5,
            pm10=pm10,
            hcho=float(hcho) / 1000,
            temp=float(temp) / 10,
            humidity=(humidity) / 10
        )
