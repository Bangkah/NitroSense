#!/usr/bin/env python3
"""
Linux NitroSense V3 – Acer Nitro V16
Standalone GUI + CLI
"""

import sys, os, psutil
from PyQt5 import QtWidgets, QtCore
try:
    import pynvml
    pynvml.nvmlInit()
    has_nv = True
except:
    has_nv = False

# ---------------- System Functions ----------------
def get_cpu_temp():
    temps = psutil.sensors_temperatures()
    if 'coretemp' in temps:
        return max([t.current for t in temps['coretemp']])
    return None

def get_gpu_temp():
    if not has_nv: return None
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

def set_fan_speed(speed):
    try:
        hwmon_path = '/sys/class/hwmon/'
        for hw in os.listdir(hwmon_path):
            fan_file = f'{hwmon_path}/{hw}/fan1_output'
            if os.path.exists(fan_file):
                with open(fan_file, 'w') as f:
                    f.write(str(speed))
                return True
    except:
        pass
    return False

def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        return f"{battery.percent}% | {'Charging' if battery.power_plugged else 'Discharging'}"
    return "N/A"

def set_performance_mode(mode):
    if mode not in ['silent', 'balanced', 'performance']: return False
    os.system(f"powerprofilesctl set {mode}")
    return True

# ---------------- GUI ----------------
class NitroSenseApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux NitroSense V3")
        self.resize(400, 300)

        self.info_label = QtWidgets.QLabel("Loading...")
        self.fan_label = QtWidgets.QLabel("Fan Speed: N/A RPM")

        self.fan_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.fan_slider.setMinimum(1000)
        self.fan_slider.setMaximum(5000)
        self.fan_slider.setValue(get_fan_speed() or 2500)
        self.fan_slider.valueChanged.connect(self.change_fan_speed)

        self.silent_btn = QtWidgets.QPushButton("Silent")
        self.balanced_btn = QtWidgets.QPushButton("Balanced")
        self.performance_btn = QtWidgets.QPushButton("Performance")
        self.silent_btn.clicked.connect(lambda: set_performance_mode('silent'))
        self.balanced_btn.clicked.connect(lambda: set_performance_mode('balanced'))
        self.performance_btn.clicked.connect(lambda: set_performance_mode('performance'))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.fan_label)
        layout.addWidget(self.fan_slider)
        layout.addWidget(self.silent_btn)
        layout.addWidget(self.balanced_btn)
        layout.addWidget(self.performance_btn)
        self.setLayout(layout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)

    def update_info(self):
        cpu = get_cpu_temp()
        gpu = get_gpu_temp()
        fan = get_fan_speed()
        battery = get_battery_status()
        self.info_label.setText(
            f"CPU Temp: {cpu if cpu else 'N/A'}°C\n"
            f"GPU Temp: {gpu if gpu else 'N/A'}°C\n"
            f"Battery: {battery}"
        )
        self.fan_label.setText(f"Fan Speed: {fan if fan else 'N/A'} RPM")

    def change_fan_speed(self, value):
        set_fan_speed(value)

# ---------------- CLI ----------------
import argparse

def main():
    parser = argparse.ArgumentParser(description="NitroSense V3 CLI/GUI")
    parser.add_argument('--gui', action='store_true')
    parser.add_argument('--cpu', action='store_true')
    parser.add_argument('--gpu', action='store_true')
    parser.add_argument('--fan', action='store_true')
    parser.add_argument('--battery', action='store_true')
    parser.add_argument('--fan-set', type=int)
    parser.add_argument('--mode', type=str)
    args = parser.parse_args()

    if args.gui:
        app = QtWidgets.QApplication(sys.argv)
        window = NitroSenseApp()
        window.show()
        sys.exit(app.exec_())

    if args.cpu: print(f"CPU Temp: {get_cpu_temp() or 'N/A'}°C")
    if args.gpu: print(f"GPU Temp: {get_gpu_temp() or 'N/A'}°C")
    if args.fan: print(f"Fan Speed: {get_fan_speed() or 'N/A'} RPM")
    if args.battery: print(f"Battery: {get_battery_status()}")
    if args.fan_set: set_fan_speed(args.fan_set)
    if args.mode: set_performance_mode(args.mode)

if __name__ == "__main__":
    main()
