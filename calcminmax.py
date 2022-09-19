
try:
    import os
    from cmath import nan
    import tkinter as tk
    from tkinter import filedialog
    import pandas as pd
    import statistics as stat
    import csv
except ModuleNotFoundError as err:
    print('[ERROR] ', err, '. Install required module with "pip" command first (python3 -m pip install <module>).')
    input('Press ENTER key to continue...')
    exit()

### VARIABLES ###
starttimes = [1800, 2400, 3000, 3600, 4200, 4800]
timestep = 599
header = ["Timeframe", "Value", "Resprate", "Heartrate", "Satrate", "Min", "Max", "Average", "Median", ]
lstexp = []

### IMPORT DIALOG ###
def import_dialog():
    global filemonitor, id
    root = tk.Tk()
    root.withdraw()
    filemonitor = filedialog.askopenfilename(filetypes=[('.csvfiles', '.csv')], title='Select monitor data')
    if not filemonitor:
        print('[ERROR] No file selected.')
        exit()
    id = input("Enter ID of measurement: ")
    lstexp.append((id))

### CSV HEADER CREATION ###
timeframe = str(starttimes[0])+"-"+str((starttimes[-1]+timestep))
csvheader1 = ["", timeframe, "","","","","","","","","","",""]
csvheader2 = ["","RESPRATE","","","","HEARTRATE","","","","SATRATE","","",""]
csvheader3 = ["ID","MIN","MAX","AVERAGE","MEDIAN","MIN","MAX","AVERAGE","MEDIAN","MIN","MAX","AVERAGE","MEDIAN"]
for i in starttimes:
    timeframe = str(i)+"-"+str(i+timestep)
    csvheader1.extend((timeframe, "","","","","","","","","","",""))
    csvheader2.extend(("RESPRATE","","","","HEARTRATE","","","","SATRATE","","",""))
    csvheader3.extend(("MIN","MAX","AVERAGE","MEDIAN","MIN","MAX","AVERAGE","MEDIAN","MIN","MAX","AVERAGE","MEDIAN"))

### IMPORT DATA ###
def import_data():
    global resp, heart, sat
    df = pd.read_csv(filemonitor, sep=',', usecols=['Rel.Time [s]', 'Infinity|RESP.RR [BREATHS_PER_MIN]', 'Infinity|ECG.HR [BEATS_PER_MIN]', 'Infinity|SPO2.SATURATION [PERCENT]'])
    resp = df['Infinity|RESP.RR [BREATHS_PER_MIN]'].tolist()
    heart = df['Infinity|ECG.HR [BEATS_PER_MIN]'].tolist()
    sat = df['Infinity|SPO2.SATURATION [PERCENT]'].tolist()
    df = 0 # clean dataframe

### CLEAN DATA ###
def clean_data_nan():
    global resp, heart, sat
    resp = [item for item in resp if not(pd.isnull(item)) == True]
    heart = [item for item in heart if not(pd.isnull(item)) == True]
    sat = [item for item in sat if not(pd.isnull(item)) == True]

### CLEAN DATA FOR UNPLAUSIBLE VALUES ###
def clean_data_unplausible():
    global resptemp, hearttemp, sattemp
    resptemp = [x for x in resptemp if x > 5]
    hearttemp = [x for x in hearttemp if x > 5]
    sattemp = [x for x in sattemp if x > 5]
    
### CALC DATA
def calc_data():
    global lstexp, resptemp, hearttemp, sattemp
    print("")
    print(f"{header[0]:<9} | {header[1]:<9} | {header[5]:<6} | {header[6]:<6} | {header[7]:<3} | {header[8]:<3}")
    print("--------- | --------- | ------ | ------ | ------- | ------")
    # COMPLETE TIMEFRAME
    resptemp = resp[starttimes[0]:(starttimes[-1]+timestep)]
    hearttemp = heart[starttimes[0]:(starttimes[-1]+timestep)]
    sattemp = sat[starttimes[0]:(starttimes[-1]+timestep)]
    clean_data_unplausible()
    respmin = min(resptemp)
    respmax = max(resptemp)
    respaverage = round(stat.mean(resptemp), 2)
    respmedian = stat.median(resptemp)
    print(f"{starttimes[0]}-{(starttimes[-1]+timestep)} | {header[2]:<9} | {respmin:<6} | {respmax:<6} | {respaverage:<7.2f} | {respmedian:<6}")
    heartmin = min(hearttemp)
    heartmax = max(hearttemp)
    heartaverage = round(stat.mean(hearttemp),2)
    heartmedian = stat.median(hearttemp)
    print(f"          | {header[3]:<9} | {heartmin:<6} | {heartmax:<6} | {heartaverage:<7.2f} | {heartmedian:<6}")
    satmin = min(sattemp)
    satmax = max(sattemp)
    sataverage = round(stat.mean(sattemp), 2)
    satmedian = stat.median(sattemp)
    print(f"          | {header[4]:<9} | {satmin:<6} | {satmax:<6} | {sataverage:<7.2f} | {satmedian:<6}")
    lstexp.extend((respmin, respmax, respaverage, respmedian, heartmin, heartmax, heartaverage, heartmedian, satmin, satmax, sataverage, satmedian))
    # TIMEFRAME SEQUENCE
    for i in starttimes:
        print("--------- | --------- | ------ | ------ | ------- | ------")
        resptemp = resp[i:(i+timestep)]
        hearttemp = heart[i:(i+timestep)]
        sattemp = sat[i:(i+timestep)]
        clean_data_unplausible()
        # RESP
        respmin = min(resptemp)
        respmax = max(resptemp)
        respaverage = round(stat.mean(resptemp), 2)
        respmedian = stat.median(resptemp)
        print(f"{i}-{i+timestep} | {header[2]:<9} | {respmin:<6} | {respmax:<6} | {respaverage:<7.2f} | {respmedian:<6}")
        # HEART
        heartmin = min(hearttemp)
        heartmax = max(hearttemp)
        heartaverage = round(stat.mean(hearttemp), 2)
        heartmedian = stat.median(hearttemp)
        print(f"          | {header[3]:<9} | {heartmin:<6} | {heartmax:<6} | {heartaverage:<7.2f} | {heartmedian:<6}")
        # SAT
        satmin = min(sattemp)
        satmax = max(sattemp)
        sataverage = round(stat.mean(sattemp), 2)
        satmedian = stat.median(sattemp)
        print(f"          | {header[4]:<9} | {satmin:<6} | {satmax:<6} | {sataverage:<7.2f} | {satmedian:<6}")
        lstexp.extend((respmin, respmax, respaverage, respmedian, heartmin, heartmax, heartaverage, heartmedian, satmin, satmax, sataverage, satmedian))

### SAVE TO CSV ###
def export_data():
    if os.path.exists("export.csv"):
        with open('export.csv', 'a') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            wr.writerow(lstexp)
    else:
        with open('export.csv', 'a') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            wr.writerow(csvheader1)
            wr.writerow(csvheader2)
            wr.writerow(csvheader3)
            wr.writerow(lstexp)

### START ###
import_dialog()
import_data()
clean_data_nan()
calc_data()
export_data()
print("")
input('Press ENTER key to continue...')
