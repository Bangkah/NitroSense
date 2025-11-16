#!/usr/bin/env python3
"""
NitroSense-like App for Acer Nitro V16 (Linux)
Version 1 – GUI + CLI
"""

import sys
import psutil
from PyQt5 import QtWidgets, QtCore

# Optional NVIDIA GPU monitoring
try:
    import pynvml
    pynvml.nvmlInit()
    has_nv = True
except:
    has_nv = False

# ------------------------
# Functions to read system
# ------------------------
def get_cpu_temp():
    temps = psutil.sensors_temperatures()
    if 'coretemp' in temps:
        core_temps = temps['coretemp']
        return max([t.current for t in core_temps])
    return None

def get_gpu_temp():
    if not has_nv:
        return None
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    return pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

def get_fan_speed():
    try:
        hwmon_path = '/sys/class/hwmon/'
        for hw in os.listdir(hwmon_path):
            fan_file = f'{hwmon_path}/{hw}/fan1_input'
            if os.path.exists(fan_file):
                with open(fan_file) as f:
                    return int(f.read().strip())
        return None
    except:
        return None

def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        return f"{battery.percent}% | {'Charging' if battery.power_plugged else 'Discharging'}"
    return "N/A"

# ------------------------
# GUI Application
# ------------------------
class NitroSenseApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux NitroSense V16")
        self.resize(400, 200)

        self.label = QtWidgets.QLabel("Loading system info...")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)  # update setiap detik

    def update_info(self):
        cpu = get_cpu_temp()
        gpu = get_gpu_temp()
        fan = get_fan_speed()
        battery = get_battery_status()
        self.label.setText(
            f"CPU Temp: {cpu if cpu else 'N/A'}°C\n"
            f"GPU Temp: {gpu if gpu else 'N/A'}°C\n"
            f"Fan Speed: {fan if fan else 'N/A'} RPM\n"
            f"Battery: {battery}"
        )

# ------------------------
# CLI handling
# ------------------------
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="NitroSense V16 CLI/GUI")
    parser.add_argument('--gui', action='store_true', help='Launch GUI')
    parser.add_argument('--cpu', action='store_true', help='Show CPU temp')
    parser.add_argument('--gpu', action='store_true', help='Show GPU temp')
    parser.add_argument('--fan', action='store_true', help='Show Fan speed')
    parser.add_argument('--battery', action='store_true', help='Show battery status')
    args = parser.parse_args()

    if args.gui:
        app = QtWidgets.QApplication(sys.argv)
        window = NitroSenseApp()
        window.show()
        sys.exit(app.exec_())

    if args.cpu:
        print(f"CPU Temp: {get_cpu_temp() or 'N/A'}°C")
    if args.gpu:
        print(f"GPU Temp: {get_gpu_temp() or 'N/A'}°C")
    if args.fan:
        print(f"Fan Speed: {get_fan_speed() or 'N/A'} RPM")
    if args.battery:
        print(f"Battery: {get_battery_status()}")

if __name__ == "__main__":
    main()
