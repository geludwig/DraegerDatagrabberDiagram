# MODULES
try:
    from cmath import nan
    import tkinter as tk
    from tkinter import filedialog
    import pandas as pd
    import matplotlib.pyplot as plt
except ModuleNotFoundError as err:
    print('[ERROR] ', err, '. Install required module with "pip" command first.')
    exit()

# IMPORT
print('[INFO] IMPORT DIALOG')
root = tk.Tk()
root.withdraw()
file = filedialog.askopenfilename()
if not file:
    print('[ERROR] No file selected, exiting.')
    exit()

# LIMITS
resprateUpper = 100
resprateLower = 50
heartrateUpper = 160
heartrateLower = 120
satrateLower = 95

# READ CSV
print('[INFO] READ CSV')
df = pd.read_csv(file, sep=',', usecols=['Rel.Time [s]', 'Infinity|RESP.RR [BREATHS_PER_MIN]', 'Infinity|ECG.HR [BEATS_PER_MIN]', 'Infinity|SPO2.SATURATION [PERCENT]'])
time = df['Rel.Time [s]'].tolist()
resprate = df['Infinity|RESP.RR [BREATHS_PER_MIN]'].tolist()
heartrate = df['Infinity|ECG.HR [BEATS_PER_MIN]'].tolist()
satrate = df['Infinity|SPO2.SATURATION [PERCENT]'].tolist()
df = 0 # clean dataframe

# REMOVE DOUBLES / NaN
print('[INFO] CLEAN DATA')
time = list(dict.fromkeys(time))
resprate = [item for item in resprate if not(pd.isnull(item)) == True]
heartrate = [item for item in heartrate if not(pd.isnull(item)) == True]
satrate = [item for item in satrate if not(pd.isnull(item)) == True]

# FIX DATA CORRUPTION (END OF FILE)
timeLen = len(time)
resprateLen = len(resprate)
heartrateLen = len(heartrate)
satrateLen = len(satrate)
if timeLen > (resprateLen or heartrateLen or satrateLen):
    print('[WARNING] DATA CORRUPTED, TRY TO FIX DATA NOW')
    csvFlag = 1
    minLen = [resprateLen, heartrateLen, satrateLen] # create list with lenghts
    minLen = min(minLen) # find smalles list
    lenFixList = [time, resprate, heartrate, satrate] # list of lists which will be shortened
    for x in lenFixList:
        xLen = len(x)
        if xLen > minLen: # if check because "del x[-n:]" needs n > 0, otherwise error
            n = xLen - minLen
            del x[-n:]
else:
    csvFlag = 0

# CALC LIMITS
print('[INFO] CALC LIMITS')
resprateLimit = [nan if resprateLower<x<resprateUpper else x for x in resprate]
heartrateLimit = [nan if heartrateLower<x<heartrateUpper else x for x in heartrate]
satrateLimit = [nan if satrateLower<x else x for x in satrate]

# PLOT
print('[INFO] PLOT DIAGRAM')
plt.plot(time, resprate, color='limegreen', label='Resprate')
plt.plot(time, resprateLimit, color='green', label='Resprate Limit')
plt.plot(time, heartrate, color='darkorange', label='Heartrate')
plt.plot(time, heartrateLimit, color='red', label='Heartrate Limit')
plt.plot(time, satrate, color='dodgerblue', label='Satrate')
plt.plot(time, satrateLimit, color='blue', label='Satrate Limit')
plt.xlabel('time')
plt.ylabel('index')
if csvFlag == 1:
    plt.legend(loc='best', fancybox=True, shadow=True, title='DATA CORRUPTED, CHECK CSV')
else:
    plt.legend(loc='best', fancybox=True, shadow=True)
plt.grid(True)
plt.show() 