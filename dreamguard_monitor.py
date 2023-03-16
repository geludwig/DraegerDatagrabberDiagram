'''Calculate vaues for monitor data.'''


if __name__ == '__main__':
    print(f">>> DREAMGUARD STARTUP\n")
    print(f"[ERROR] Start program with '_main.py'")
    exit()


import traceback
import math
import datetime
import dreamguard_global

class Monitor:
    """calculate clean monitor data
    create lists for diagramm
    return  self.resprate
            self.heartrate
            self.satrate
            self.resprate_lim
            self.heartrate_lim
            self.satrate_lim
    """

    def __init__(self, unix_time, reltime, resprate, heartrate, satrate):

        resprate_max = dreamguard_global.RESPRATE_MAX
        resprate_min = dreamguard_global.RESPRATE_MIN
        heartrate_max = dreamguard_global.HEARTRATE_MAX
        heartrate_min = dreamguard_global.HEARTRATE_MIN
        satrate_min = dreamguard_global.SATRATE_MIN

        self.timestamp = []
        self.reltime = []
        self.resprate = []
        self.heartrate = []
        self.satrate = []

        # calc timestamp from unix time
        try:
            for x in unix_time:
                temp = (datetime.datetime.fromtimestamp(x/1000).strftime('%H:%M:%S.%f')) # extract h, m, s, ms from unix
                self.timestamp.append(datetime.datetime.strptime(temp,'%H:%M:%S.%f')) # covert to datetime object (date is now 1970, but does not matter)
        except:
            print(traceback.format_exc())
            raise

        try:
            # clean time, resp, heart, sat lists
            # lists may contain no value for one specific time (nan),
            #   also relative times may exists more than one time
            # the first while loop looks out if next relative time value
            #   is greater than the old relative time value
            # the while loops inside the while loop append the data from
            #   resprate, satrate, heartrate to new lists because
            #   a correct value for these lists may not exist in
            #   the first line of one specific relative time,
            #   it looks out for the next line
            #   if the relative time value matches the current time value.
            #   if a valid value is found,
            #   it appends this value to the new list.
            #   if no valid value is found and the next line is not
            #   the current time value, it appends the last value
            #   from the newly created list
            i = 0
            while i < len(reltime)-1:
                # append new rel time when different than old rel time
                if i == 0 or reltime[i] > self.reltime[-1]:
                    self.reltime.append(reltime[i])
                    # while reltime has same relative time, append value to
                    #   list if not nan, then break loop (remove empty values)
                    j = i
                    while True:
                        if j == len(reltime):
                            self.resprate.append(self.resprate[-1])
                            break
                        if reltime[j] == reltime[i]:
                            if math.isnan(resprate[j]) is False:
                                self.resprate.append(resprate[j])
                                break
                        else:
                            self.resprate.append(self.resprate[-1])
                            break
                        j += 1

                    j = i
                    while True:
                        if j == len(reltime):
                            self.heartrate.append(self.heartrate[-1])
                            break
                        if reltime[j] == reltime[i]:
                            if math.isnan(heartrate[j]) is False:
                                self.heartrate.append(heartrate[j])
                                break
                        else:
                            self.heartrate.append(self.heartrate[-1])
                            break
                        j += 1

                    j = i
                    while True:
                        if j == len(reltime):
                            self.satrate.append(self.satrate[-1])
                            break
                        if reltime[j] == reltime[i]:
                            if math.isnan(satrate[j]) is False:
                                self.satrate.append(satrate[j])
                                break
                        else:
                            self.satrate.append(self.satrate[-1])
                            break
                        j += 1
                i += 1
        except:
            print(f"[ERROR] {traceback.format_exc()}")
            raise

        try:
            # calc limits
            self.resprate_lim = [math.nan if resprate_min < x < resprate_max else x for x in self.resprate]
            self.heartrate_lim = [math.nan if heartrate_min < x < heartrate_max else x for x in self.heartrate]
            self.satrate_lim = [math.nan if satrate_min < x else x for x in self.satrate]
            # seconds to milliseconds
            self.reltime = [i * 1000 for i in self.reltime]
        except:
            print(f"[ERROR] {traceback.format_exc()}")
            raise
