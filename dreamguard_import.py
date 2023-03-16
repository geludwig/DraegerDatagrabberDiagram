"""Import files of monitor and sensor (CSV and TXT)."""


if __name__ == '__main__':
    print(f">>> DREAMGUARD STARTUP\n")
    print(f"[ERROR] Start program with '_main.py'")
    exit()


import traceback
import tkinter as tk
import tkinter.filedialog as filedialog
import pathlib
import pandas as pd
import numpy as np


class Monitor:
    """Import CSV file from datagrabber / monitor.
    Returns:    self.unix_time
                self.reltime
                self.resprate
                self.heartrate
                self.satrate
                self.folderpath

    Disclaimer: This object does not not really meet the requirements
      to be defined as an object, because it is not called with any arguments.
    """

    def __init__(self):
        self.err_flag = False
        self.unix_time = []
        self.reltime = []
        self.resprate = []
        self.heartrate = []
        self.satrate = []

        print(f"[INFO] Switch to selection window and choose monitor.csv file.")
        root = tk.Tk()
        root.withdraw()
        file_monitor = filedialog.askopenfilename(filetypes=[('.csvfiles', '.csv')], title='Select monitor.csv')
        root.destroy()

        if file_monitor:
            self.folderpath = pathlib.Path(file_monitor).parent
            try:
                # pd.read_csv() has built-in "with open" function. See:
                # https://pandas.pydata.org/docs/user_guide/io.html
                # https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv
                # https://stackoverflow.com/questions/53649222/should-i-use-with-openfile-if-i-pd-read-csv
                dataframe = pd.read_csv(file_monitor, sep=',', usecols=['Time [ms]', 'Rel.Time [s]', 'Infinity|RESP.RR [BREATHS_PER_MIN]', 'Infinity|ECG.HR [BEATS_PER_MIN]', 'Infinity|SPO2.SATURATION [PERCENT]'])
                self.unix_time = dataframe['Time [ms]'].tolist()
                self.reltime = dataframe['Rel.Time [s]'].tolist()
                self.resprate = dataframe['Infinity|RESP.RR [BREATHS_PER_MIN]'].tolist()
                self.heartrate = dataframe['Infinity|ECG.HR [BEATS_PER_MIN]'].tolist()
                self.satrate = dataframe['Infinity|SPO2.SATURATION [PERCENT]'].tolist()
                dataframe = 0
                print(f"[INFO] Monitor: {file_monitor}")
            except:
                print(f"[ERROR] {traceback.format_exc()}")
                raise
        else:
            print(f"FileError: No file selected.")
            raise Exception


class Sensor:
    """Import TXT file from Draeger sensor.
    Returns:    self.hourshex
                self.minuteshex
                self.secondshex
                self.millieshex
                self.accx1hex
                self.accx2hex
                self.accy1hex
                self.accy2hex
                self.accz1hex
                self.accz2hex
                self.gyrox1hex
                self.gyrox2hex
                self.gyroy1hex
                self.gyroy2hex
                self.gyroz1hex
                self.gyroz2hex
    """

    def __init__(self, folderpath):

        self.hourshex = []
        self.minuteshex = []
        self.secondshex = []
        self.millieshex = []
        self.accx1hex = []
        self.accx2hex = []
        self.accy1hex = []
        self.accy2hex = []
        self.accz1hex = []
        self.accz2hex = []
        self.gyrox1hex = []
        self.gyrox2hex = []
        self.gyroy1hex = []
        self.gyroy2hex = []
        self.gyroz1hex = []
        self.gyroz2hex = []

        print(f"[INFO] Switch to selection window and choose sensor.txt file.")
        root = tk.Tk()
        root.withdraw()
        file_sensor = filedialog.askopenfilename(initialdir=folderpath, filetypes=[('.textfiles', '.txt')], title='Select sensor.txt')
        root.destroy()

        if file_sensor:
            try:
                sensordata = np.genfromtxt(file_sensor, dtype=str, delimiter=' ')
                self.hourshex = sensordata[:, 0]
                self.minuteshex = sensordata[:, 1]
                self.secondshex = sensordata[:, 2]
                self.millieshex = sensordata[:, 3]
                self.accx1hex = sensordata[:, 4]
                self.accx2hex = sensordata[:, 5]
                self.accy1hex = sensordata[:, 6]
                self.accy2hex = sensordata[:, 7]
                self.accz1hex = sensordata[:, 8]
                self.accz2hex = sensordata[:, 9]
                self.gyrox1hex = sensordata[:, 10]
                self.gyrox2hex = sensordata[:, 11]
                self.gyroy1hex = sensordata[:, 12]
                self.gyroy2hex = sensordata[:, 13]
                self.gyroz1hex = sensordata[:, 14]
                self.gyroz2hex = sensordata[:, 15]
                sensordata = 0
                print(f"[INFO] Sensor: {file_sensor}")
            except:
                print(f"[ERROR] {traceback.format_exc()}")
                raise
        else:
            print(f"FileError: No file selected.")
            raise Exception
