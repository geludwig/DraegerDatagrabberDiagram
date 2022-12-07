# Calculate sensor data

# dependencies
import dg_init
#import dg_global


# import modules
import os
import time
import datetime
import serial
import serial.tools.list_ports


### COMMANDS ###
erase = b'\x44\x0A'
freq = b'\x66\x0A' # 26Hz
startlog = b'\x12\x34\x0A'
stoplog = b'\x46\x16\x00\x34\x10\x0A'
starttransfer = b'\x88\x0A\x12\x34\x0A'
deviceoff = b'\x11\x0A'
stopstr = "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF"
#timelog = b'\x64\xHH\xMM\xSS\xMS\x0A'


### OPEN FILE ###
def openFile():
    print(">>> SELECT FILE NAME")
    global filename
    global flag
    overwrite = ""
    filenameGood = False
    while filenameGood == False:
        filename = input("\nINPUT FILE NAME AND PRESS ENTER: ")
        filename = filename + ".txt"
        filenameGood = True
        if os.path.exists(filename):
            overwrite = input("FILE EXISTS - OVERWRITE? [(y)es / (n)o / any to exit]: ")
            if overwrite == "y":
                os.remove(filename)
            elif overwrite == "n":
                filenameGood = False
            else:
                print("\nNO FILE NAME SPECIFIED")
                input("\nPRESS ENTER TO CONTINUE")
                flag = True
    return flag
            
### LIST SERIAL PORTS ###
def listSerial():
    global ports
    global flag
    timeout = 20
    timeoutStr = str(timeout)
    if command == 4:
        reqPorts = 2
    else:
        reqPorts = 1
    print(">>> SELECT PORTS")
    print("")
    ports = serial.tools.list_ports.comports()
    while (len(ports) < reqPorts) and (timeout >= 0):
        ports = serial.tools.list_ports.comports()
        print("WAITING FOR ",  reqPorts - len(ports), " MORE PORTS (" + timeoutStr + "s)", end="\r")
        timeout = timeout-1
        if timeout < 10:
            timeoutStr = "0"+str(timeout)
        else:
            timeoutStr = str(timeout)
        time.sleep(1)
    if len(ports) >= reqPorts:
        i = 1
        for p in ports:
            print(i, " : ", p)
            i = i+1
    else:
        print("\nNOT ENOUGH PORTS AVAILABLE")
        input("\nPRESS ENTER TO CONTINUE")
        flag = True
    return flag

### OPEN SERIAL CONSOLE ###
def openConsole():
    global console
    global flag
    # SELECT PORT
    print("")
    while True:
        try:
            consoleport = input("[INFO] Enter number of 'Silicon Labs (CP2102)': ")
            consoleport = str(ports[int(consoleport)-1]) # ID from str to int, then search in list "ports", then convert to string
            consoleport = consoleport.split(" - ")
            consoleport = consoleport[0]
            break
        except:
            pass
    # OPEN PORT
    try:
        console = serial.Serial()
        console.port = consoleport
        console.baudrate = 115200
        console.parity = serial.PARITY_NONE
        console.stopbits = serial.STOPBITS_ONE
        console.bytesize = serial.EIGHTBITS
        console.xonxoff=True
        console.open()
    except serial.SerialException as err:
        print("\n[ERROR] : ",err)
        input("\nPRESS ENTER TO CONTINUE")
        flag = True
    except:
        print("\n[ERROR] : unknown")
        input("\nPRESS ENTER TO CONTINUE")
        flag = True
    return flag

### OPEN SERIAL RECEIVER ###
def openReceiver():
    global receiver
    global flag
    # SELECT PORT
    print("")
    while True:
        try:
            receiverport = input("[INFO] Enter number of 'Serial Cable': ")
            receiverport = str(ports[int(receiverport)-1]) # ID from str to int, then search in list "ports", then convert to string
            receiverport = receiverport.split(" - ")
            receiverport = receiverport[0]
            break
        except:
            pass
    # OPEN PORT
    try:
        receiver = serial.Serial()
        receiver.port = receiverport
        receiver.baudrate = 921600
        receiver.timeout = 1
        receiver.parity = serial.PARITY_NONE
        receiver.stopbits = serial.STOPBITS_ONE
        receiver.bytesize = serial.EIGHTBITS
        receiver.xonxoff = False
        receiver.rts = False
        receiver.dtr = False
        receiver.open()
    except serial.SerialException as err:
        print("\n[ERROR] : ",err)
        input("\nPRESS ENTER TO CONTINUE")
        flag = True
    except:
        print("\n[ERROR] : unknown")
        input("\nPRESS ENTER TO CONTINUE")
        flag = True
    return flag

### START LOG ###
def startLog():
    print(">>> START LOG")
    global flag
    try:
        console.write(erase)
        time.sleep(3)
        console.write(freq)
        time.sleep(3)
        now = datetime.datetime.now()
        h = int(str(now.hour), 16)
        m = int(str(now.minute), 16)
        s = int(str(now.second), 16)
        ms = int(str(now.strftime('%f')[:-4]), 16)
        settime = bytes([h, m, s, ms])
        console.write(b'\x64')
        console.write(settime)
        console.write(b'\x0A')
        console.write(startlog)
        console.close()
        print("\nOK")
        input("\nPRESS ENTER TO CONTINUE")
    except serial.SerialException as err:
        print("\n[ERROR] : ",err)
        input("\nPRESS ENTER TO CONTINUE")
        flag = True
    except:
        print("\n[ERROR] : unknown")
        input("\nPRESS ENTER TO CONTINUE")
        flag = True
    return flag

### STOP LOG ###
def stopLog():
    print(">>> STOP LOG")
    global flag
    try:
        console.write(stoplog)
        console.close()
        print("\nOK")
        input("\nPRESS ENTER TO CONTINUE")
    except serial.SerialException as err:
        print("\nERROR] : ",err)
        input("\nPRESS ENTER TO CONTINUE")
        flag = True
    except:
        print("\n[ERROR] : unknown")
        input("\nPRESS ENTER TO CONTINUE")
        flag = True
    return flag
        

#### DEVICE OFF ###
def offDevice():
    print(">>> DEVICE OFF")
    global flag
    try:
        console.write(deviceoff)
        console.close()
        print("\nOK")
        input("\nPRESS ENTER TO CONTINUE")
    except serial.SerialException as err:
        print("\n[ERROR] : ",err)
        input("\nPRESS ENTER TO CONTINUE")
        flag = True
    except:
        print("\n[ERROR] : unknown")
        input("\nPRESS ENTER TO CONTINUE")
        flag = True
    return flag

### TRANSFER DATA ###
def transferData():
    global flag
    global linesTransfer

    DEBUG = True
    linesTransfer = 0
    i = 0

    print(">>> TRANSFER DATA")
    print("\nTRANSFERING ...")
    print("0", end ="\r")

    # FILE OPEN
    try:
        file = open(filename, "a")
    except Exception as err:
        print("[ERROR]", err)

    # SEND START COMMAND
    try:
        console.write(starttransfer)
        console.close()
    except Exception as err:
        print("[ERROR]", err)

    # LOOP SERIAL
    while True:
        try:
            byte = receiver.read(22) # wait till 22 bytes in buffer then write to byte
            hexstr = byte.hex(' ', 1).upper() # bytes to hex [str with delimiter space and split every byte and capital hex letters]
            if hexstr == stopstr: # STOP: if string matches stopstr [end of file]
                input("\n[INFO] End of data. Press ENTER to continue.")
                break
            elif len(hexstr) == 65: # SAVE: string has 22 bytes and no stop condition
                file.write(hexstr + "\n")
                i = i+1
                print(i, end="\r")
            elif len(hexstr) < 65: # STOP: if string smaller than 22 bytes [read() timeout]
                input("\n[INFO] End of stream. Press ENTER to continue.")
                break
        except Exception as err:
            print("\n[ERROR] : ",err)
            input("[INFO] Press ENTER to continue.")
            flag = True
            break

    try:
        receiver.close()
        file.flush() # force write from buffer to file
        file.close()
    except Exception as err:
        print("\n[ERROR]", err)
        input("PRESS ENTER TO CONTINUE")
        flag = True
    linesTransfer = i-1

    return flag

### TRUNC DATA ###
def truncData():
    global flag
    try:
        file = open(filename, 'r+')
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        file.writelines(lines[:-1])
        file.close()
    except Exception as err:
        print("[ERROR] : ",err)
        input("PRESS ENTER TO CONTINUE")
        flag = True
    return flag

### CHECK DREAMGUARD DATA INTEGRETY ###
def testData():
    print(">>> CHECK DATA INTEGRITY")
    print("")
    global flag
    i = 1
    try:
        file = open(filename, 'r')
        lines = file.readlines()
        if len(lines) >= 2:
            hourold = int((lines[1])[:2], 16) # first 2 chars of first line to int
            try:
                for x in lines:
                    hour = int(x[:2], 16)
                    if hour == hourold:
                        print(i,"/",linesTransfer, end="\r")
                    elif hour == (hourold+1):
                        print(i,"/",linesTransfer, end="\r")
                    elif hour == 0 and hourold == 24:
                        print(i,"/",linesTransfer, end="\r")
                    else:
                        raise Exception
                    hourold = hour
                    i = i+1
                print("\n\nOK")
                input("\nPRESS ENTER TO CONTINUE")
            except Exception as err:
                print("[ERROR] : ",err)
                input("PRESS ENTER TO CONTINUE")
                flag = True
        else:
            print("\n\nFILE EMPTY")
            input("\nPRESS ENTER TO CONTINUE")
    except Exception as err:
        print("[ERROR] : ",err)
        input("PRESS ENTER TO CONTINUE")
        flag = True
    return flag       


### SELECT COMMAND ###
def gui():
    print(">>> DREAMGUARD MANAGER")
    print("\n1 : START LOG")
    print("2 : STOP LOG")
    print("3 : DEVICE OFF")
    print("4 : TRANSFER DATA")
    print("0 : RETURN")
    print("")


### CALL FUNCTIONS ###
def main_sensor():
    global command, flag

    command = -1
    flag = False
    while command == -1:

        dg_init.clear()
        gui()

        while True:
            try:
                command = input("ENTER NUMBER TO SELECT COMMAND: ")
                command = int(command)
                if -1 < command < 5:
                    break
            except:
                pass

        if command == 1:
            dg_init.clear()
            if flag == False: flag = listSerial()
            if flag == False: flag = openConsole()
            dg_init.clear()
            if flag == False: flag = startLog()
        elif command == 2:
            dg_init.clear()
            if flag == False: flag = listSerial()
            if flag == False: flag = openConsole()
            dg_init.clear()
            if flag == False: flag = stopLog()

        elif command == 3:
            dg_init.clear()
            if flag == False: flag = listSerial()
            if flag == False: flag = openConsole()
            dg_init.clear()
            if flag == False: flag = offDevice()
        elif command == 4:
            dg_init.clear()
            if flag == False: flag = listSerial()
            if flag == False: flag = openConsole()
            if flag == False: flag = openReceiver()
            dg_init.clear()
            if flag == False: flag = openFile()
            dg_init.clear()
            if flag == False: flag = transferData()
            if flag == False: flag = truncData()
            dg_init.clear()
            if flag == False: flag = testData()
        elif command == 0:
            break
        else:
            print("\n[ERROR] : unknown")
            input("\nPRESS ENTER TO EXIT")
            exit()

        flag = False
        command = -1