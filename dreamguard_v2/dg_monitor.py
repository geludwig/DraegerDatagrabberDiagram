# Calculate monitor data

# dependencies
import dg_global

# import modules
import math
import pandas as pd
import datetime
import time

# variables
hertz = 26
resprateUpper = 80
resprateLower = 35
heartrateUpper = 200
heartrateLower = 80
satrateLower = 80

# calc monitor
def calc(monitor_unix_time, monitor_reltime, resprate, heartrate, satrate ):

    monitor_timestamp = []
    monitor_reltime_norm = []
    resprate_norm = []
    heartrate_norm = []
    satrate_norm = []

    # calc timestamp from unix time
    for x in monitor_unix_time:
        temp = (datetime.datetime.fromtimestamp(x/1000).strftime('%H:%M:%S.%f')) # extract h, m, s, ms from unix
        monitor_timestamp.append(datetime.datetime.strptime(temp,'%H:%M:%S.%f')) # covert to datetime object (date is now 1970, but does not matter)

    #print(monitor_timestamp[0])
    #print(type(monitor_timestamp[0]))

    # clean time, resp, heart, sat lists
    i = 0
    while i < len(monitor_reltime)-1:

        # append new rel time when different than old rel time
        if i == 0 or monitor_reltime[i] > monitor_reltime_norm[-1]:
            monitor_reltime_norm.append(monitor_reltime[i])
        
            # while monitor_reltime has same relative time, append value to list if != nan and then break loop (remove empty values)
            j = i
            while True:
                if monitor_reltime[j] == monitor_reltime[i]:
                    if math.isnan(resprate[j]) == False:
                        resprate_norm.append(resprate[j])
                        break
                else:
                    #print("[ERROR] Resprate  missing. Time:", monitor_reltime_norm[-1])
                    resprate_norm.append(resprate_norm[-1])
                    break
                j += 1

            j = i
            while True:
                if monitor_reltime[j] == monitor_reltime[i]:
                    if math.isnan(heartrate[j]) == False:
                        heartrate_norm.append(heartrate[j])
                        break
                else:
                    #print("[ERROR] Heartrate missing. Time:", monitor_reltime_norm[-1])
                    heartrate_norm.append(heartrate_norm[-1])
                    break
                j += 1

            j = i
            while True:
                if monitor_reltime[j] == monitor_reltime[i]:
                    if math.isnan(satrate[j]) == False:
                        satrate_norm.append(satrate[j])
                        break
                else:
                    #print("[ERROR] Satrate   missing. Time:", monitor_reltime_norm[-1])
                    satrate_norm.append(satrate_norm[-1])
                    break
                j += 1

        i += 1

    # calc limits
    resprate_lim = [math.nan if resprateLower<x<resprateUpper else x for x in resprate_norm]
    heartrate_lim = [math.nan if heartrateLower<x<heartrateUpper else x for x in heartrate_norm]
    satrate_lim = [math.nan if satrateLower<x else x for x in satrate_norm]

    # seconds to milliseconds
    monitor_reltime_norm = [i * 1000 for i in monitor_reltime_norm]

    # RETURN
    return monitor_timestamp, monitor_reltime_norm, resprate_norm, heartrate_norm, satrate_norm, resprate_lim, heartrate_lim, satrate_lim