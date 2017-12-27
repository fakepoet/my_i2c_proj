#!/usr/bin/python

import smbus
import time

# Define some device parameters
I2C_ADDR = 0x27  # I2CLCD device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

LCD_BACKLIGHT = 0x08  # On
# LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Cycle constants
C_DELAY = 5


class LCD1206(object):
    def __init__(self):
        # Open I2C interface
        # bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
        self.bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

    def lcd_init(self):
        # Initialise display
        self.lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
        time.sleep(E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command

        bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

        # High bits
        self.bus.write_byte(I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        # Low bits
        self.bus.write_byte(I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(E_DELAY)
        self.bus.write_byte(I2C_ADDR, (bits | ENABLE))
        time.sleep(E_PULSE)
        self.bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
        time.sleep(E_DELAY)

    def lcd_string(self, message, line):
        # Send string to display
        message = message.ljust(LCD_WIDTH, " ")

        self.lcd_byte(line, LCD_CMD)

        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)

    def lcd_message(self, message):
        from itertools import izip
        msg_list = message.split('\n')[:2]
        for msg, line in izip(msg_list, [LCD_LINE_1, LCD_LINE_2]):
            self.lcd_string(msg, line)

    def lcd_clear(self):
        self.lcd_byte(0x01, LCD_CMD)

    def lcd_cycle(self, *cls_list, **kwargs):
        from utils import get_methods_list
        delay = kwargs.get('delay') or C_DELAY
        while True:
            for data_class in cls_list:
                st = data_class()
                for func_name in get_methods_list(data_class):
                    msg = getattr(st, func_name)()
                    self.lcd_clear()
                    self.lcd_message(msg)
                    time.sleep(delay)

    def lcd_greet(self, msg=None, delay=C_DELAY):
        self.lcd_message(msg or 'Hello,\n        Master')
        time.sleep(delay)


if __name__ == '__main__':
    from utils import Statuses, SensorData
    # Initialise display
    dev = LCD1206()
    dev.lcd_init()
    dev.lcd_greet()
    try:
        dev.lcd_cycle(Statuses, SensorData)
    except KeyboardInterrupt:
        pass
    except Exception:
        raise
    finally:
        dev.lcd_byte(0x01, LCD_CMD)
