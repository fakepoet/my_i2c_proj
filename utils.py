# coding: utf-8

from datetime import datetime
import commands
import psutil


def get_cpu_temp():
    cpu_tmp = open('/sys/class/thermal/thermal_zone0/temp')
    res = cpu_tmp.read()
    cpu_tmp.close()
    cpu_tmp = res

    gpu_tmp = commands.getoutput('vcgencmd measure_temp|awk -F= \'{print $2}\'').replace('\'C', '')
    gpu_tmp = float(gpu_tmp)
    gpu_temp = 'GPU_TMP: {:.2f} C'.format(gpu_tmp)
    cpu_temp = 'CPU_TMP: {:.2f} C\n'.format(float(cpu_tmp) / 1000)
    return cpu_temp + gpu_temp


def get_time_now():
    cur = datetime.now().strftime('    %H:%M:%S\n   %Y-%m-%d')
    return cur


def get_ip_info():
    wlan0_info = psutil.net_if_addrs().get('wlan0', [])
    ip_info = wlan0_info[0] if wlan0_info else 'NOT FOUND'
    return 'IP_ADDRESS: \n' + ip_info.address


def get_cpu_usage():
    message = 'CPU_USAGE:\n'
    per = ' ' * 10 + str(psutil.cpu_percent()) + '%'
    return message + per


def get_mem_info():
    total = commands.getoutput('free -m|grep Mem:|awk \'{print $2}\'')
    used = commands.getoutput('free -m|grep Mem:|awk \'{print $3}\'')
    message = 'MEM USAGE: \n'
    usage = '{}/{}   {:.2f}%'.format(used, total, float(used) / float(total) * 100)
    return message + usage
