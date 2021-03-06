# coding: utf-8

from datetime import datetime
import commands
import psutil


def get_methods_list(cls):
    import inspect
    method_list = inspect.getmembers(cls, predicate=inspect.ismethod)
    return [x[0] for x in method_list if x[0] != '__init__']


class Statuses(object):
    def get_cpu_temp(self):
        cpu_tmp = open('/sys/class/thermal/thermal_zone0/temp')
        res = cpu_tmp.read()
        cpu_tmp.close()
        cpu_tmp = res

        gpu_tmp = commands.getoutput('vcgencmd measure_temp|awk -F= \'{print $2}\'').replace('\'C', '')
        gpu_tmp = float(gpu_tmp)
        gpu_temp = 'GPU_TMP: {:.2f}{}C'.format(gpu_tmp, chr(0xDF))
        cpu_temp = 'CPU_TMP: {:.2f}{}C\n'.format(float(cpu_tmp) / 1000, chr(0xDF))
        return cpu_temp + gpu_temp

    def get_time_now(self):
        cur = datetime.now().strftime('    %H:%M:%S\n   %Y-%m-%d')
        return cur

    def get_ip_info(self):
        wlan0_info = psutil.net_if_addrs().get('wlan0', [])
        ip_info = wlan0_info[0] if wlan0_info else 'NOT FOUND'
        return 'IP_ADDRESS: \n' + ip_info.address

    def get_cpu_usage(self):
        message = 'CPU_USAGE:\n'
        per = ' ' * 10 + str(psutil.cpu_percent()) + '%'
        return message + per

    def get_mem_info(self):
        total = commands.getoutput('free -m|grep Mem:|awk \'{print $2}\'')
        used = commands.getoutput('free -m|grep Mem:|awk \'{print $3}\'')
        message = 'MEM USAGE: \n'
        usage = '{}/{}   {:.2f}%'.format(used, total, float(used) / float(total) * 100)
        return message + usage


class SensorData(object):

    def __init__(self):
        from sensors.bmp_180 import sensor
        from sensors.DHT_12 import dht_12
        self.bmp_180 = sensor
        self.dht_12 = dht_12

    def get_temp(self):
        return 'Temp_BMP:\n' + '{:.2f} {}C'.format(self.bmp_180.read_temperature(), chr(0xDF)).rjust(16)

    def get_pressure(self):
        return 'Pressure:\n' + '{:.2f} hPa'.format(float(self.bmp_180.read_pressure()) / 100).rjust(16)

    def get_altitude(self):
        return 'Altitude:\n' + '{:.2f} m'.format(self.bmp_180.read_altitude()).rjust(16)

    def get_sea_level_pressure(self):
        return 'Sealevel Pressure:\n' + '{:.2f} hPa'.format(
            float(self.bmp_180.read_sealevel_pressure()) / 100
        ).rjust(16)


class PMS5003(object):
    def __init__(self):
        from sensors.PMS5003ST import PMS5003 as P
        self.data = P.get_data()

    def get_pm2_5(self):
        pm2_5 = self.data['pm2_5']
        return 'PM2.5:(35:75)\n' + '{:.2f} ug/m3'.format(pm2_5).rjust(16)

    def get_pm10(self):
        pm10 = self.data['pm10']
        return 'PM10:(max:50)\n' + '{:.2f} ug/m3\n'.format(pm10).rjust(16)

    def get_pm1_0(self):
        pm1_0 = self.data['pm1_0']
        return 'PM1.0:\n' + '{:.2f} ug/m3\n'.format(pm1_0).rjust(16)

    def get_hcho(self):
        hcho = self.data['hcho']
        return 'HCHO:(max:0.08)\n' + '{:.2f} mg/m3'.format(hcho).rjust(16)

    def get_temp_and_humidity(self):
        temp = self.data['temp']
        humidity = self.data['humidity']
        msg1 = 'Temp:' + '{:.2f} {}C\n'.format(temp, chr(0xDF)).rjust(11)
        msg2 = 'Humi:' + '{:.2f}%'.format(humidity).rjust(11)
        return msg1 + msg2

# def getShort(data, index):
#     # return two bytes from data as a signed 16-bit value
#     return c_short((data[index] << 8) + data[index + 1]).value


# def getUshort(data, index):
#     # return two bytes from data as an unsigned 16-bit value
#     return (data[index] << 8) + data[index + 1]
