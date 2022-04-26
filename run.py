### MODULES ###
try:
    import urllib.request
    import os.path
    import tkinter as tk
except ModuleNotFoundError as err:
    print('[ERROR] ', err, '. Install required module with "pip" command first (e.g. python3 -m pip install <module>).')
    exit()

### GET PAGE ###
try:
    urlversion = urllib.request.urlopen('https://raw.githubusercontent.com/geludwig/DreamGuardAndDatagrabber/main/script.py')
    urlversion = urlversion.read()
    versionweb = [int(s) for s in urlversion.split() if s.isdigit()]
    versionweb = versionweb[0]
except:
    print('[ERROR] web request error, exiting.')
    exit()

# NO SCRIPT IN CURRENT DIR
if (os.path.exists('script.py') is False):
    try:
        print('[INFO] Downloading python script.')
        urlscript = 'https://raw.githubusercontent.com/geludwig/DreamGuardAndDatagrabber/main/script.py'
        urllib.request.urlretrieve(urlscript, filename='script.py')
        #filename, headers = urllib.request.urlretrieve(urlscript, filename='test.py')
    except:
        print('[ERROR] web request error, exiting.')
        exit()

# CHECK VERSION IF SCRIPT IS AVAILABLE
else:
    with open('script.py', "r") as file:
        versionscript = int(file.readline().strip())
# VERSION MATCH, NOTHING TO DO
        if versionweb == versionscript:
            print('[INFO] All files up to date.')
            os.system('python3 script.py')
# NEW VERSION AVAILABLE, UPDATE BOX, DOWNLOAD NW SCRIPT
        elif versionweb > versionscript:
            root= tk.Tk()
            root.geometry('300x100')
            root.resizable(False, False)
            root.title('UPDATE SCRIPT?')

            def updateYes():
                root.destroy()
                try:
                    print('[INFO] Downloading updated python script.')
                    urlscript = 'https://raw.githubusercontent.com/geludwig/DreamGuardAndDatagrabber/main/script.py'
                    urllib.request.urlretrieve(urlscript, filename='script.py')
                    os.system('python3 script.py')
                except:
                    print('[ERROR] web request error, exiting.')
                    exit()

            def updateNo():
                root.destroy()
                os.system('python3 script.py')

            buttonYes = tk.Button (root, text='YES',command=updateYes)
            buttonNo = tk.Button (root, text='NO',command=updateNo)
            buttonYes.pack(pady=10)
            buttonNo.pack()
            root.mainloop()

# VERSION EXCEPTION
        else:
            print('Something went wrong.')

# EXIT
print('[INFO] Exit.')
