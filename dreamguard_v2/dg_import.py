# Import functions


# dependencies
import dg_global


# import modules
import tkinter as tk
import tkinter.filedialog as filedialog
import pandas as pd
import numpy as np
import pathlib



# import monitor file
def monitor():

    monitor_unix_time = monitor_reltime = resprate = heartrate = satrate = []

    print("[INFO] Switch to selection window and choose monitor.csv file.")
    root = tk.Tk()
    root.withdraw()
    file_monitor = filedialog.askopenfilename(filetypes=[('.csvfiles', '.csv')], title='Select monitor.csv')
    folderpath = pathlib.Path(file_monitor).parent
    root.destroy()

    if file_monitor:
        try:
            df = pd.read_csv(file_monitor, sep=',', usecols=['Time [ms]', 'Rel.Time [s]', 'Infinity|RESP.RR [BREATHS_PER_MIN]', 'Infinity|ECG.HR [BEATS_PER_MIN]', 'Infinity|SPO2.SATURATION [PERCENT]'])
            monitor_unix_time = df['Time [ms]'].tolist()
            monitor_reltime = df['Rel.Time [s]'].tolist()
            resprate = df['Infinity|RESP.RR [BREATHS_PER_MIN]'].tolist()
            heartrate = df['Infinity|ECG.HR [BEATS_PER_MIN]'].tolist()
            satrate = df['Infinity|SPO2.SATURATION [PERCENT]'].tolist()
            df = 0
            print("[INFO] Monitor: ", file_monitor)
        except:
            print("[ERROR] Cant read file_tarpos.")
            input("[INFO] Press ENTER to continue...")
            dg_global.flag = True
    else:
        print("[WARNING] No file_tarpos selected.")
        input("[INFO] Press ENTER to continue...")
        dg_global.flag = True
    return folderpath, monitor_unix_time, monitor_reltime, resprate, heartrate, satrate


# import sensor
def sensor(folderpath):
    
    hourshex = minuteshex = secondshex = millsechex = accx1hex = accx2hex = accy1hex = accy2hex = accz1hex = accz2hex = gyrox1hex = gyrox2hex = gyroy1hex = gyroy2hex = gyroz1hex = gyroz2hex = []

    print("[INFO] Switch to selection window and choose sensor.txt file.")
    root = tk.Tk()
    root.withdraw()
    file_sensor = filedialog.askopenfilename(initialdir=folderpath, filetypes=[('.textfiles', '.txt')], title='Select sensor.txt')
    root.destroy()

    if file_sensor:
        try:
            sensordata = np.genfromtxt(file_sensor, dtype=str, delimiter=' ')
            hourshex = sensordata[:,0]
            minuteshex = sensordata[:,1]
            secondshex = sensordata[:,2]
            millsechex = sensordata[:,3]
            accx1hex = sensordata[:,4]
            accx2hex = sensordata[:,5]
            accy1hex = sensordata[:,6]
            accy2hex = sensordata[:,7]
            accz1hex = sensordata[:,8]
            accz2hex = sensordata[:,9]
            gyrox1hex = sensordata[:,10]
            gyrox2hex = sensordata[:,11]
            gyroy1hex = sensordata[:,12]
            gyroy2hex = sensordata[:,13]
            gyroz1hex = sensordata[:,14]
            gyroz2hex = sensordata[:,15]
            sensordata = 0
            print("[INFO] Sensor: ", file_sensor)
        except:
            print("[ERROR] Cant read file_tarpos.")
            input("[INFO] Press ENTER to continue...")
            dg_global.flag = True
    else:
        print("[WARNING] No file_tarpos selected.")
        input("[INFO] Press ENTER to continue...")
        dg_global.flag = True
    return hourshex, minuteshex, secondshex, millsechex, accx1hex, accx2hex, accy1hex, accy2hex, accz1hex, accz2hex, gyrox1hex, gyrox2hex, gyroy1hex, gyroy2hex, gyroz1hex, gyroz2hex