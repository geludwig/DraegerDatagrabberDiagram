# Calculate sensor data

# dependencies
import dg_global

# import modules
import pandas as pd
import numpy as np
import threading
import time
import datetime


def calc(hertz, hourshex, minuteshex, secondshex, millsechex, accx1hex, accx2hex, accy1hex, accy2hex, accz1hex, accz2hex, gyrox1hex, gyrox2hex, gyroy1hex, gyroy2hex, gyroz1hex, gyroz2hex):


    # calc rel time
    def calc_rel_time():
        global sensor_reltime
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

        sensor_reltime = [int(x) for x in timesensorfloat]
        print(end='\n')
        return sensor_reltime


    # calc timestamp
    def calc_sensor_timestamp():
        global sensor_timestamp
        sensor_timestamp= []
        millisec_unix = []

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
        millisec = convert_hex(millsechex)

        for x in millisec:
            temp = int(x*(1000/hertz))
            if temp == 0:
                temp = "000"
            elif temp < 100:
                temp = "0" + str(temp)
            millisec_unix.append(temp)

        # convert string to datetime obj timestamp
        for hours, minutes, seconds, millisec_unix in zip(hours, minutes, seconds, millisec_unix):
            temp = '{}:{}:{}.{}'.format(hours, minutes, seconds, millisec_unix)
            sensor_timestamp.append(datetime.datetime.strptime(temp,'%H:%M:%S.%f'))
        
        return sensor_timestamp


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

    #threadcount = threading.active_count()
    thread1 = threading.Thread(target=calc_rel_time)
    thread2 = threading.Thread(target=calc_sensor_timestamp)
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

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()

    # RETURN
    return sensor_timestamp, sensor_reltime, accx, accy, accz, gyrox, gyroy, gyroz
