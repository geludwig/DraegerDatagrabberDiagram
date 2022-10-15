
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
    input('Press ENTER key to exit...')
    exit()

### VARIABLES ###
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

### USER INPUT TIMESTEPS ###
def input_starttimes():
    global starttimeList
    global endtimeList
    starttimeList = []
    endtimeList = []
    starttime = 0
    endtime = 0
    while True:
        try:
            starttime = int(input("Enter starttime (nothing if finished): "))
        except:
            break
        endtime = int(input("Enter endtime: "))
        starttimeList.append(starttime)
        endtimeList.append(endtime)

### CSV HEADER CREATION ###
def create_header():
    global csvheader1
    global csvheader2
    global csvheader3
    csvheader1 = [""]
    csvheader2 = [""]
    csvheader3 = ["ID"]
    for x in starttimeList:
        timeframe = str(x)+"-"+str(endtimeList[starttimeList.index(x)])
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
    # TIMEFRAME SEQUENCE
    for x in starttimeList:
        resptemp = resp[x:(endtimeList[starttimeList.index(x)])]
        hearttemp = heart[x:(endtimeList[starttimeList.index(x)])]
        sattemp = sat[x:(endtimeList[starttimeList.index(x)])]
        clean_data_unplausible()
        # RESP
        respmin = min(resptemp)
        respmax = max(resptemp)
        respaverage = round(stat.mean(resptemp), 2)
        respmedian = stat.median(resptemp)
        # HEART
        heartmin = min(hearttemp)
        heartmax = max(hearttemp)
        heartaverage = round(stat.mean(hearttemp), 2)
        heartmedian = stat.median(hearttemp)
        # SAT
        satmin = min(sattemp)
        satmax = max(sattemp)
        sataverage = round(stat.mean(sattemp), 2)
        satmedian = stat.median(sattemp)
        lstexp.extend((respmin, respmax, respaverage, respmedian, heartmin, heartmax, heartaverage, heartmedian, satmin, satmax, sataverage, satmedian))

### SAVE TO CSV ###
def export_data():
    if os.path.exists("export.csv"):
        with open('export.csv', 'a') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            wr.writerow("")
            wr.writerow(csvheader1)
            wr.writerow(csvheader2)
            wr.writerow(csvheader3)
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
input_starttimes()
create_header()
import_data()
clean_data_nan()
calc_data()
export_data()
print("")
input('Press ENTER key to continue...')
