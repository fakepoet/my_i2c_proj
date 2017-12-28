# coding: utf-8
import serial
import time
import struct


class PMS5003(object):

    @staticmethod
    def get_data():
        while True:
            # 获得接收缓冲区字符
            ser = serial.Serial("/dev/ttyS0", 9600)
            count = ser.inWaiting()
            print count
            if count >= 32:
                recv = ser.read(32)
                print recv
                print type(recv)
                (sign1, sign2, frame_length, pm1_0_cf, pm2_5_cf, pm10_cf, pm1_0,
                 pm2_5, pm10, cnt_03, cnt_05, cnt_10, cnt_25, cnt_50, cnt_100,
                 hcho, temp, humidity, reserve, version, checksum) = struct.unpack('>bb' + 'H' * 19, recv)

                if sign1 == 0x42 and sign2 == 0x4d:
                    break
            time.sleep(1)
        return dict(
            pm1_0=pm1_0,
            pm2_5=pm2_5,
            pm10=pm10,
            hcho=float(hcho) / 1000,
            temp=float(temp) / 10,
            humidity=(humidity) / 10
        )
