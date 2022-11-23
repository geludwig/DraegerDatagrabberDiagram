# Calculate monitor data

# dependencies
import dg_global

# import modules
import matplotlib as plt
import numpy as np

# align start times
def align_clock(hertz, monitor_timestamp, monitor_reltime_norm, resprate_norm, heartrate_norm, satrate_norm, resprate_lim, heartrate_lim, satrate_lim, sensor_timestamp, sensor_reltime, accx, accy, accz, gyrox, gyroy, gyroz):

    maxtime = 60
    imonitor = 0
    isensor = 0

    if monitor_timestamp[0] < sensor_timestamp[0]: # monitor first, then sensor (monitor smaller)
        # if monitor was started before sensor
        # monitor data every 1 second, sensor every <hertz> millisecond
        # first step to check monitor array which element is still smaller than sensor array, and delete all elements before from monitor array
        # second step to check sensor array  which element is still smaller than monitor array, and delete all elements before from sensor array
        # reason for second step is finer resolution from sensor, worst case after first step there can be a delta of 1 sec
        while (imonitor <= maxtime) and (monitor_timestamp[imonitor] < sensor_timestamp[0]):
            imonitor = imonitor+1
        if imonitor > 0:
            monitor_timestamp = monitor_timestamp[imonitor:] # from front
        if sensor_timestamp[0] < monitor_timestamp[0]:
            while (isensor  <= hertz) and (sensor_timestamp[isensor ] < monitor_timestamp[0]):
                isensor  += 1
            if isensor > 0:
                sensor_timestamp = sensor_timestamp[isensor:] # from front

    if sensor_timestamp[0] < monitor_timestamp[0]: # sensor first, then monitor (sensor smaller)
        while sensor_timestamp[isensor] < monitor_timestamp[0]:
            isensor += 1
        if isensor > 0:
            sensor_timestamp = sensor_timestamp[(isensor-1):] # from front
    #print('[INFO] Aligned start times - monitor:', monitor_timestamp[0], ' sensor:', sensor_timestamp[0])

    monitor_reltime_norm = monitor_reltime_norm[imonitor:]
    resprate_norm = resprate_norm[imonitor:]
    heartrate_norm = heartrate_norm[imonitor:]
    satrate_norm = satrate_norm[imonitor:]
    resprate_lim = resprate_lim[imonitor:]
    heartrate_lim = heartrate_lim[imonitor:]
    satrate_lim = satrate_lim[imonitor:]

    sensor_reltime = sensor_reltime[isensor:]
    accx = accx[isensor:]
    accy = accy[isensor:]
    accz = accz[isensor:]
    gyrox = gyrox[isensor:]
    gyroy = gyroy[isensor:]
    gyroz = gyroz[isensor:]

    return monitor_reltime_norm, resprate_norm, heartrate_norm, satrate_norm, resprate_lim, heartrate_lim, satrate_lim, sensor_reltime, accx, accy, accz, gyrox, gyroy, gyroz