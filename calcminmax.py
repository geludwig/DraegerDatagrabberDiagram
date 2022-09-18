
try:
    from cmath import nan
    import tkinter as tk
    from tkinter import filedialog
    import pandas as pd
    import statistics as stat
except ModuleNotFoundError as err:
    print('[ERROR] ', err, '. Install required module with "pip" command first (python3 -m pip install <module>).')
    input('Press ENTER key to continue...')
    exit()

### VARIABLES ###
starttimes = [1800, 2400, 3000, 3600, 4200, 4800]
timestep = 599
header = ["Timeframe", "Value", "Resprate", "Heartrate", "Satrate", "Min", "Max", "Average", "Median", ]

### IMPORT DIALOG ###
def import_dialog():
    global filemonitor
    root = tk.Tk()
    root.withdraw()
    filemonitor = filedialog.askopenfilename(filetypes=[('.csvfiles', '.csv')], title='Select monitor data')
    if not filemonitor:
        print('[ERROR] No file selected.')
        exit()

### IMPORT DATA ###
def import_data():
    global resp, heart, sat
    df = pd.read_csv(filemonitor, sep=',', usecols=['Rel.Time [s]', 'Infinity|RESP.RR [BREATHS_PER_MIN]', 'Infinity|ECG.HR [BEATS_PER_MIN]', 'Infinity|SPO2.SATURATION [PERCENT]'])
    resp = df['Infinity|RESP.RR [BREATHS_PER_MIN]'].tolist()
    heart = df['Infinity|ECG.HR [BEATS_PER_MIN]'].tolist()
    sat = df['Infinity|SPO2.SATURATION [PERCENT]'].tolist()
    df = 0 # clean dataframe

### SPLIT DATA ###
def clean_data():
    global resp, heart, sat
    resp = [item for item in resp if not(pd.isnull(item)) == True]
    heart = [item for item in heart if not(pd.isnull(item)) == True]
    sat = [item for item in sat if not(pd.isnull(item)) == True]

### CALC DATA
def calc_data():
    print(f"{header[0]:<9} | {header[1]:<9} | {header[5]:<6} | {header[6]:<6} | {header[7]:<3} | {header[8]:<3}")
    print("--------- | --------- | ------ | ------ | ------- | ------")

    # COMPLETE TIMEFRAME
    resptemp = resp[starttimes[0]:(starttimes[-1]+timestep)]
    hearttemp = heart[starttimes[0]:(starttimes[-1]+timestep)]
    sattemp = sat[starttimes[0]:(starttimes[-1]+timestep)]

    respmin = min(resptemp)
    respmax = max(resptemp)
    respaverage = stat.mean(resptemp)
    respmedian = stat.median(resptemp)
    print(f"{starttimes[0]}-{(starttimes[-1]+timestep)} | {header[2]:<9} | {respmin:<6} | {respmax:<6} | {respaverage:<7.2f} | {respmedian:<6}")
    heartmin = min(hearttemp)
    heartmax = max(hearttemp)
    heartaverage = stat.mean(hearttemp)
    heartmedian = stat.median(hearttemp)
    print(f"          | {header[3]:<9} | {heartmin:<6} | {heartmax:<6} | {heartaverage:<7.2f} | {heartmedian:<6}")
    satmin = min(sattemp)
    satmax = max(sattemp)
    sataverage = stat.mean(sattemp)
    satmedian = stat.median(sattemp)
    print(f"          | {header[4]:<9} | {satmin:<6} | {satmax:<6} | {sataverage:<7.2f} | {satmedian:<6}")
    
    # TIMEFRAME SEQUENCE
    print("--------- | --------- | ------ | ------ | ------- | ------")
    for i in starttimes:
        resptemp = resp[i:(i+timestep)]
        hearttemp = heart[i:(i+timestep)]
        sattemp = sat[i:(i+timestep)]
        # RESP
        respmin = min(resptemp)
        respmax = max(resptemp)
        respaverage = stat.mean(resptemp)
        respmedian = stat.median(resptemp)
        print(f"{i}-{i+timestep} | {header[2]:<9} | {respmin:<6} | {respmax:<6} | {respaverage:<7.2f} | {respmedian:<6}")
        # HEART
        heartmin = min(hearttemp)
        heartmax = max(hearttemp)
        heartaverage = stat.mean(hearttemp)
        heartmedian = stat.median(hearttemp)
        print(f"          | {header[3]:<9} | {heartmin:<6} | {heartmax:<6} | {heartaverage:<7.2f} | {heartmedian:<6}")
        # SAT
        satmin = min(sattemp)
        satmax = max(sattemp)
        sataverage = stat.mean(sattemp)
        satmedian = stat.median(sattemp)
        print(f"          | {header[4]:<9} | {satmin:<6} | {satmax:<6} | {sataverage:<7.2f} | {satmedian:<6}")


### START ###
import_dialog()
import_data()
clean_data()
calc_data()
