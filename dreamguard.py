import serial
import serial.tools.list_ports
import os
import time
import datetime


### COMMANDS ###
erase = b'\x44\x0A'
freq = b'\x66\x0A' # 26Hz
startlog = b'\x12\x34\x0A'
stoplog = b'\x46\x16\x00\x34\x10\x0A'
deviceoff = b'\x11\x0A'
stopstr = "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF"
#timelog = b'\x64\xHH\xMM\xSS\xMS\x0A'

### CLEAR CONSOLE ###
def clear():
    os.system('cls' if os.name=='nt' else 'clear')


### SELECT COMMAND ###
def selCommand():
    global command
    print("1 : START LOG")
    print("2 : STOP LOG")
    print("3 : DEVICE OFF")
    print("4 : TRANSFER DATA")
    print("5 : EXIT")
    command = input("ENTER NUMBER TO SELECT COMMAND: ")
    command = int(command)


### OPEN FILE ###
def openFile():
    global filename
    print("")
    overwrite = ""
    filenameGood = False

    while filenameGood == False:
        filename = input("INPUT FILE NAME:")
        filename = filename + ".txt"
        filenameGood = True
        if os.path.exists(filename):
            overwrite = input("FILE EXISTS - OVERWRITE? [(y)es / (n)o / any to exit]: ")
            if overwrite == "y":
                os.remove(filename)
            elif overwrite == "n":
                filenameGood = False
            else:
                input("PRESS ENTER TO EXIT")
                exit()
            

### LIST SERIAL PORTS ###
def listSerial():
    global ports
    global iports
    print("")
    ports = serial.tools.list_ports.comports()
    if len(ports) >= 1:
        print("PORTS AVAILABLE:")
        i = 0
        for p in ports:
            print(i, " : ", p)
            i = i+1
        iports = i
    else:
        print("NO PORTS AVAILABLE")
        input("PRESS ENTER TO EXIT")
        exit()


### OPEN SERIAL CONSOLE ###
def openConsole():
    global console
    # SELECT PORT
    consoleport = input("ENTER NUMBER OF 'Silicon Labs': ")
    consoleport = str(ports[int(consoleport)]) # ID from str to int, then search in list "ports", then convert to string
    consoleport = consoleport.split(" - ")
    consoleport = consoleport[0]
    # OPEN PORT
    console = serial.Serial()
    console.port = consoleport
    console.baudrate = 115200
    console.parity = serial.PARITY_NONE
    console.stopbits = serial.STOPBITS_ONE
    console.bytesize = serial.EIGHTBITS
    console.xonxoff=True
    console.open()


### OPEN SERIAL RECEIVER ###
def openReceiver():
    global receiver
    # SELECT PORT
    receiverport = input("ENTER NUMBER OF 'Serial Cable': ")
    receiverport = str(ports[int(receiverport)]) # ID from str to int, then search in list "ports", then convert to string
    receiverport = receiverport.split(" - ")
    receiverport = receiverport[0]
    # OPEN PORT
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


### START LOG ###
def startLog():
    print("")
    print("STARTING LOG")
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
    print("OK")
    input("PRESS ENTER TO CONTINUE")


### STOP LOG ###
def stopLog():
    print("")
    print("STOP LOG")
    console.write(stoplog)
    console.close()
    print("OK")
    input("PRESS ENTER TO CONTINUE")


#### DEVICE OFF ###
def offDevice():
    print("")
    print("DEVICE OFF")
    console.write(deviceoff)
    console.close()
    print("OK")
    input("PRESS ENTER TO CONTINUE")


### TRANSFER DATA ###
def transferData():
    print("")
    stop = False
    i = 0
    print("TRANSFER DATA")
    # FILE OPEN
    file = open(filename, "a")
    # SEND START COMMAND
    startcommand = b'\x88\x0A\x12\x34\x0A'
    console.write(startcommand)
    console.close()
    # LOOP SERIAL
    while stop is False:
        byte = receiver.read(22) # wait till 22 bytes in buffer then write to byte
        hexstr = byte.hex(' ', 1).upper() # bytes to hex [str with delimiter space and split every byte and capital hex letters]
        if hexstr == stopstr: # STOP if string matches stopstr [end of file]
            stop = True
            print("\nEND OF FILE REACHED")
        elif len(hexstr) != 65: # STOP if string smaller than 22 bytes [read() timeout]
            stop = True
            print("\nEND OF FILE REACHED")
        elif len(hexstr) == 65: # SAVE: string has 22 bytes and no stop condition
            file.write(hexstr + "\n")
            i = i+1
            print(i, end="\r")
        else:
            print("\nERROR")
            input("PRESS ENTER TO EXIT")
            exit()
    file.close()
    receiver.close()


### TRUNC DATA ###
def truncData():
    file = open(filename, 'r+')
    lines = file.readlines()
    file.seek(0)
    file.truncate()
    file.writelines(lines[:-1])
    file.close()


### CHECK DREAMGUARD DATA INTEGRETY ###
def testData():
    print("")
    print("CHECK DATA INTEGRITY")
    i = 0
    file = open(filename, 'r')
    lines = file.readlines()

    if len(lines) >= 2:
        hourold = int((lines[1])[:2], 16) # first 2 chars of first line to int
        for x in lines:
            hour = int(x[:2], 16)
            if hour == hourold:
                print(i, end="\r")
            elif hour == (hourold+1):
                print(i, end="\r")
            else:
                print("ERROR")
                input("PRESS ENTER TO EXIT")
                exit()
            hourold = hour
            i = i+1
        print("\nOK")
        input("PRESS ENTER TO CONTINUE")
    else:
        print("\nFILE EMPTY")
        input("PRESS ENTER TO CONTINUE")


### CALL FUNCTIONS ###
command = 0
while command == 0:
    clear()
    selCommand()
    if command == 1:
        listSerial()
        openConsole()
        startLog()
        command = 0
    elif command == 2:
        listSerial()
        openConsole()
        stopLog()
        command = 0
    elif command == 3:
        listSerial()
        openConsole()
        offDevice()
        command = 0
    elif command == 4:
        listSerial()
        if iports < 2:
            print("\nNOT ENOUGH COM PORTS")
            input("PRESS ENTER TO CONTINUE")
            command = 0
        else:
            openConsole()
            openReceiver()
            openFile()
            transferData()
            truncData()
            testData()
            command = 0
    elif command == 5:
        exit()
    else:
        command = 0