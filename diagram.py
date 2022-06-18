6

### MODULES ###
try:
    from cmath import nan
    import tkinter as tk
    from tkinter import filedialog
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    import sys
    import threading
    import time
    from datetime import datetime
except ModuleNotFoundError as err:
    print('[ERROR] ', err, '. Install required module with "pip" command first (e.g. python3 -m pip install <module>).')
    input('Press any key to continue...')
    exit()


### USER DEFINED VARIABLES / LIMITS ###
hertz = 26
resprateUpper = 80
resprateLower = 35
heartrateUpper = 200
heartrateLower = 80
satrateLower = 80


### IMPORT DIALOG ###
def import_dialog():
    global filemonitor, filesensor

    root = tk.Tk()
    root.withdraw()

    # MONITOR
    print('[INFO] Import dialog.')
    filemonitor = filedialog.askopenfilename(filetypes=[('.csvfiles', '.csv')], title='Select monitor data')
    if not filemonitor:
        print('[ERROR] No file selected.')
        exit()

    time.sleep(0.5) # tiomeout between file dialoges to minimize false mouse click

    # SENSOR
    filesensor = filedialog.askopenfilename(filetypes=[('.textfiles', '.txt')], title='Select sensor data')
    if not filesensor:
        print('[ERROR] No file selected.')
        exit()

    root.destroy()

    print('[INFO] Monitor file: ', filemonitor)
    print('[INFO] Sensor file: ', filesensor)
    return filemonitor, filesensor


### MONITOR DATA ###
def calc_monitor():
    global csvflag, clockmonitor, timemonitor, resprate, heartrate, satrate, respratelim, heartratelim, satratelim

    # READ CSV
    df = pd.read_csv(filemonitor, sep=',', usecols=['Time [ms]', 'Rel.Time [s]', 'Infinity|RESP.RR [BREATHS_PER_MIN]', 'Infinity|ECG.HR [BEATS_PER_MIN]', 'Infinity|SPO2.SATURATION [PERCENT]'])
    clockmonitor = df['Time [ms]'].tolist()
    timemonitor = df['Rel.Time [s]'].tolist()
    resprate = df['Infinity|RESP.RR [BREATHS_PER_MIN]'].tolist()
    heartrate = df['Infinity|ECG.HR [BEATS_PER_MIN]'].tolist()
    satrate = df['Infinity|SPO2.SATURATION [PERCENT]'].tolist()
    df = 0 # clean dataframe

    # CALC UNIX TIME
    clockmonitor = list(dict.fromkeys(clockmonitor))
    clockmonitor  = [(x/1000) for x in clockmonitor]
    clockmonitor = [(datetime.fromtimestamp(x).strftime('%H:%M:%S.%f')[:-3]) for x in clockmonitor]

    # CALC REL TIME
    timemonitor = list(dict.fromkeys(timemonitor))
    timemonitor = [i * 1000 for i in timemonitor] # multiply witch ms to match sensor data 

    # REMOVE DOUBLES / NaN
    resprate = [item for item in resprate if not(pd.isnull(item)) == True]
    heartrate = [item for item in heartrate if not(pd.isnull(item)) == True]
    satrate = [item for item in satrate if not(pd.isnull(item)) == True]

    # FIX DATA CORRUPTION (END OF FILE)
    timeLen = len(timemonitor)
    resprateLen = len(resprate)
    heartrateLen = len(heartrate)
    satrateLen = len(satrate)
    if timeLen > (resprateLen or heartrateLen or satrateLen):
        print('[WARNING] Fixing corrupted monitor data.')
        csvflag = 1
        minLen = [resprateLen, heartrateLen, satrateLen] # create list with lenghts
        minLen = min(minLen) # find smalles list
        lenFixList = [timemonitor, resprate, heartrate, satrate] # list of lists which will be shortened
        for x in lenFixList:
           xLen = len(x)
           if xLen > minLen: # if check because "del x[-n:]" needs n > 0, otherwise error
                n = xLen - minLen
                del x[-n:]
    else:
        csvflag = 0

    # CALC LIMITS
    respratelim = [nan if resprateLower<x<resprateUpper else x for x in resprate]
    heartratelim = [nan if heartrateLower<x<heartrateUpper else x for x in heartrate]
    satratelim = [nan if satrateLower<x else x for x in satrate]

    # RETURN
    return csvflag, clockmonitor, timemonitor, resprate, heartrate, satrate, respratelim, heartratelim, satratelim


### SENSOR DATA ###
def calc_sensor():

    # IMPORT
    print('[INFO] Loading, please wait.')
    sensordata = np.genfromtxt(filesensor, dtype=str, delimiter=' ')
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

    # CALC UNIX TIME
    def calc_clock_sensor():
        global clocksensor

        def convert_hex(arrayhex):
            global listclock
            listclock = []
            for x in arrayhex:
                x = int(str(x), 16)
                listclock.append(x)
            return listclock

        hours = convert_hex(hourshex)
        hours = [('%02d' % (x,)) for x in hours]
        minutes = convert_hex(minuteshex)
        minutes = [('%02d' % (x,)) for x in minutes]
        seconds = convert_hex(secondshex)
        seconds = [('%02d' % (x,)) for x in seconds]
        millsec = convert_hex(millsechex)
        millsec = [int(x*(1000/hertz)) for x in millsec]

        clocksensor = ['{}:{}:{}.{}'.format(hours, minutes, seconds, millsec) for hours, minutes, seconds, millsec in zip(hours, minutes, seconds, millsec)] # DOES NOT WORK, LEADING ZERO MISSING
        return clocksensor

    # CALC REL TIME
    def calc_rel_time():
        global timesensor
        length = len(millsechex)
        timesensorfloat = []
        calcsec = 0
        calcmill = 0
        intervall = 1000/hertz
        i = 0

        while i < length: # calc ms and add one second after overflow -> [..., 961, 1000, 1038, ... 1961, 2000, 2038, ...]
            if calcmill >=999:
                calcmill = 0
                calcsec = calcsec + 1000
            calctime = calcsec + calcmill
            timesensorfloat.append(calctime)
            calcmill = calcmill + intervall
            i = i+1
            progress = 100 / (length / i)
            print('[INFO] Progress:', '%.1f' % progress, '%', end='\r') # progress bar

        timesensor = [int(x) for x in timesensorfloat]
        print(end='\n')
        return timesensor

    # ACCELERATION
    # X
    def calc_acc_x():
        global accx
        arrayint = []
        accxhex = [str(m)+str(n) for m,n in zip(accx1hex,accx2hex)]
        for x in accxhex:
            x = int(str(x), 16)
            if x > 32767:
                x -= 65536
            arrayint.append(x)
        accx = [x / 16384 for x in arrayint]
        return accx
    # Y
    def calc_acc_y():
        global accy
        arrayint = []
        accyhex = [str(m)+str(n) for m,n in zip(accy1hex,accy2hex)]
        for x in accyhex:
            x = int(str(x), 16)
            if x > 32767:
                x -= 65536
            arrayint.append(x)
        accy = [x / 16384 for x in arrayint]
        return accy
    # Z
    def calc_acc_z():
        global accz
        arrayint = []
        acczhex = [str(m)+str(n) for m,n in zip(accz1hex,accz2hex)]
        for x in acczhex:
            x = int(str(x), 16)
            if x > 32767:
                x -= 65536
            arrayint.append(x)
        accz = [x / 16384 for x in arrayint]
        return accz

    # GYRO
    #X
    def calc_gyro_x():
        global gyrox
        arrayint = []
        gyroxhex = [str(m)+str(n) for m,n in zip(gyrox1hex,gyrox2hex)]
        for x in gyroxhex:
            x = int(str(x), 16)
            if x > 32767:
                x -= 65536
            arrayint.append(x)
        gyrox = [x / 132 for x in arrayint]
        return gyrox
    #Y
    def calc_gyro_y():
        global gyroy
        arrayint = []
        gyroyhex = [str(m)+str(n) for m,n in zip(gyroy1hex,gyroy2hex)]
        for x in gyroyhex:
            x = int(str(x), 16)
            if x > 32767:
                x -= 65536
            arrayint.append(x)
        gyroy = [x / 132 for x in arrayint]
        return gyroy
    #Z
    def calc_gyro_z():
        global gyroz
        arrayint = []
        gyrozhex = [str(m)+str(n) for m,n in zip(gyroz1hex,gyroz2hex)]
        for x in gyrozhex:
            x = int(str(x), 16)
            if x > 32767:
                x -= 65536
            arrayint.append(x)
        gyroz = [x / 132 for x in arrayint]
        return gyroz

    # MULTITHREADING
    threadcount = threading.active_count()
    thread1 = threading.Thread(target=calc_rel_time)
    thread2 = threading.Thread(target=calc_clock_sensor)
    thread3 = threading.Thread(target=calc_gyro_x)
    thread4 = threading.Thread(target=calc_gyro_y)
    thread5 = threading.Thread(target=calc_gyro_z)
    thread6 = threading.Thread(target=calc_acc_x)
    thread7 = threading.Thread(target=calc_acc_y)
    thread8 = threading.Thread(target=calc_acc_z)
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()

    while (threading.active_count() > threadcount):
        time.sleep(1)

    # RETURN
    return timesensor, clocksensor, accx, accy, accz, gyrox, gyroy, gyroz


### ALIGN LISTS CLOCK ###
def align_clock():
    global clockmonitor, clocksensor, imonitor, isensor
    maxtime = 60
    imonitor = 0
    isensor = 0

    cmtmp = clockmonitor[0]
    cstmp = clocksensor[0]

    if cmtmp < cstmp: # monitor first, then sensor (monitor smaller)
        # if monitor was started before sensor
        # monitor data every 1 second, sensor every <hertz> millisecond
        # first step to check monitor array which element is still smaller than sensor array, and delete all elements before from monitor array
        # second step to check sensor array  which element is still smaller than monitor array, and delete all elements before from sensor array
        # reason for second step is finer resolution from sensor, worst case after first step there can be a delta of 1 sec
        while (imonitor <= maxtime) and (clockmonitor[imonitor] < clocksensor[0]):
            imonitor = imonitor+1
        if imonitor > 0:
            clockmonitor = clockmonitor[imonitor:] # from front
        if clocksensor[0] < clockmonitor[0]:
            while (isensor  <= hertz) and (clocksensor[isensor ] < clockmonitor[0]):
                isensor  = isensor +1
            if isensor > 0:
                clocksensor = clocksensor[isensor:] # from front

    if cstmp < cmtmp: # sensor first, then monitor (sensor smaller)
        while (isensor <= (60*hertz)) and (clocksensor[isensor] < clockmonitor[0]):
            isensor = isensor+1
        if isensor > 0:
            clocksensor = clocksensor[isensor:] # from front

    print('[INFO] Aligned start times - monitor:', clockmonitor[0], ' sensor:', clocksensor[0])
    return imonitor, isensor


### CUT LISTS ###
def cut_lists():
    global timemonitor, resprate, heartrate, satrate, respratelim, heartratelim, satratelim
    global timesensor, accx, accy, accz, gyrox, gyroy, gyroz

    timemonitor = timemonitor[imonitor:]
    resprate = resprate[imonitor:]
    heartrate = heartrate[imonitor:]
    satrate = satrate[imonitor:]
    respratelim = respratelim[imonitor:]
    heartratelim = heartratelim[imonitor:]
    satratelim = satratelim[imonitor:]

    timesensor = timesensor[isensor:]
    accx = accx[isensor:]
    accy = accy[isensor:]
    accz = accz[isensor:]
    gyrox = gyrox[isensor:]
    gyroy = gyroy[isensor:]
    gyroz = gyroz[isensor:]

    return timemonitor, resprate, heartrate, satrate, respratelim, heartratelim, satratelim, timesensor, accx, accy, accz, gyrox, gyroy, gyroz


### PLOT ###
def calc_plot():
    # FUNC SNAP CURSOR
    class SnaptoCursor(object):
        def __init__(self, ax, x, y):
            self.ax = ax
            self.ly = ax.axvline(color='k', alpha=0.2)  # the vert line
            self.marker, = ax.plot([0],[0], marker="o", color="crimson", zorder=3) 
            self.x = x
            self.y = y
            self.txt = ax.text(0.7, 0.9, '')

        def mouse_move(self, event):
            if not event.inaxes: return
            x, y = event.xdata, event.ydata
            indx = np.searchsorted(self.x, [x])[0]
            try:
                x = self.x[indx]
                y = self.y[indx]
            except:
                x = self.x[0]
                y = self.y[0]
            self.ly.set_xdata(x)
            self.marker.set_data([x],[y])
            self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
            self.txt.set_position((x,y))
            self.ax.figure.canvas.draw_idle()

    # FUNC SELECT GRAPH
    def on_pick(event):
        legend = event.artist
        isVisible = legend.get_visible()
        graphs[legend].set_visible(not isVisible)
        legend.set_visible(not isVisible)
        fig.canvas.draw()

    # DEFINE PLOT PROPERTIES
    fig, (ax1, ax2)  = plt.subplots(2, sharex=True)
    ax1.ticklabel_format(useOffset=False, style='plain')
    ax1.grid(True)
    ax2.grid(True)
    ax2.set_xlabel('Time in ms')
    ax1.set_ylabel('Scale1')
    ax2.set_ylabel('gravitational force OR degrees per sec')

    # DEFINE GRAPH PROPERTIES
    ax1.plot(timemonitor, resprate, color='limegreen', label='resprate')
    ax1.plot(timemonitor, respratelim, color='green')
    ax1.plot(timemonitor, heartrate, color='darkorange', label='heartrate')
    ax1.plot(timemonitor, heartratelim, color='red')
    ax1.plot(timemonitor, satrate, color='dodgerblue', label='satrate')
    ax1.plot(timemonitor, satratelim, color='blue')

    axplt, = ax2.plot(timesensor, accx, color='red', label='acc x', linewidth=0.6)
    ayplt, = ax2.plot(timesensor, accy, color='green', label='acc y', linewidth=0.6)
    azplt, = ax2.plot(timesensor, accz, color='blue', label='acc z', linewidth=0.6)
    gxplt, = ax2.plot(timesensor, gyrox, color='red', label='gyro x', linewidth=0.6)
    gyplt, = ax2.plot(timesensor, gyroy, color='green', label='gyro y', linewidth=0.6)
    gzplt, = ax2.plot(timesensor, gyroz, color='blue', label='gyro z', linewidth=0.6)

    # DEFINE LEGENDS
    ax1.legend(loc='upper right')
    legend2 = ax2.legend(loc='upper right')
    axplt_legend2, ayplt_legend2, azplt_legend2, gxplt_legend2, gyplt_legend2, gzplt_legend2 = legend2.get_lines()

    # DEFINE PICKER
    arraylegend = [axplt_legend2, ayplt_legend2, azplt_legend2, gxplt_legend2, gyplt_legend2, gzplt_legend2]
    for x in arraylegend:
        x.set_picker(True)
        x.set_pickradius(10)

    # DEFINE GRAPHS
    graphs = {}
    graphs[axplt_legend2] = axplt
    graphs[ayplt_legend2] = ayplt
    graphs[azplt_legend2] = azplt
    graphs[gxplt_legend2] = gxplt
    graphs[gyplt_legend2] = gyplt
    graphs[gzplt_legend2] = gzplt

    # DEFAULT HIDE ALL AX2 GRAPHS
    for x in arraylegend:
        graphs[x].set_visible(False)
        x.set_visible(False)

    # CONNECT PLOT
    cursor = SnaptoCursor(ax1, timemonitor, resprate)
    cursor1 = SnaptoCursor(ax1, timemonitor, heartrate)
    cursor2 = SnaptoCursor(ax1, timemonitor, satrate)
    plt.connect('motion_notify_event', cursor.mouse_move)  
    plt.connect('motion_notify_event', cursor1.mouse_move)
    plt.connect('motion_notify_event', cursor2.mouse_move)
    plt.connect('pick_event', on_pick)

    # DRAW PLOT
    print('[INFO] Drawing plot.')
    plt.show() 


### CALL FUNCTIONS ###
import_dialog()
calc_monitor()
calc_sensor()
align_clock()
cut_lists()
calc_plot()
