### MODULES ###
try:
    import urllib.request
    import os.path
    import sys
    import tkinter as tk
except ModuleNotFoundError as err:
    print('[ERROR] ', err, '. Install required module with "pip" command first (e.g. python3 -m pip install <module>).')
    exit()

### WEBPAGE ###
urlscript = 'https://raw.githubusercontent.com/geludwig/DreamGuardAndDatagrabber/main/script.py'

### CATCH MACOS CA EXCEPTION
try:
    urllib.request.urlopen(urlscript)
except:
    if sys.platform == 'darwin':
        print('[ERROR] System runs MacOS. May need to install CA certificates first.')

### UPDATE / DOWNLOAD SCRIPT ###
# NO SCRIPT IN DIR
if (os.path.exists('script.py') is False):
    try:
        urllib.request.urlretrieve(urlscript, filename='script.py')
        os.system('python3 script.py')
    except urllib.error.HTTPError as e:
        print('[ERROR] HTTP error: ', e)
        print('[ERROR] Can not download script.')
        exit()
    except urllib.error.URLError as e:
        print('[ERROR] URL error: ', e)
        print('[ERROR] Can not download script.')
        exit()

# SCRIPT IN DIR
else:
    # GET WEB VERSION
    try:
        urlversion = urllib.request.urlopen(urlscript)
        urlversion = urlversion.read()
        versionweb = [int(s) for s in urlversion.split() if s.isdigit()]
        versionweb = versionweb[0]
    except urllib.error.HTTPError as e:
        print('[ERROR] HTTP error: ', e)
        print('[WARNING] Can not verify version, fallback to local file.')
        os.system('python3 script.py')
    except urllib.error.URLError as e:
        print('[ERROR] URL error: ', e)
        print('[WARNING] Can not verify version, fallback to local file.')
        os.system('python3 script.py')

    # GET SCRIP VERSION
    with open('script.py', "r") as file:
        versionscript = int(file.readline().strip())
        if versionweb == versionscript:
            # VERSION MATCH, NOTHING TO DO
            print('[INFO] All files up to date.')
            os.system('python3 script.py')
        elif versionweb > versionscript:
            # NEW VERSION AVAILABLE, UPDATE BOX, DOWNLOAD NW SCRIPT
            print('[INFO] New version available.')
            root= tk.Tk()
            root.geometry('300x100')
            root.resizable(False, False)
            root.title('UPDATE SCRIPT?')

            def updateYes():
                root.destroy()
                try:
                    print('[INFO] Updating python script.')
                    urllib.request.urlretrieve(urlscript, filename='script.py')
                    os.system('python3 script.py')
                except urllib.error.HTTPError as e:
                    print('[ERROR] HTTP error: ', e)
                    exit()
                except urllib.error.URLError as e:
                    print('[ERROR] URL error: ', e)
                    exit()

            def updateNo():
                root.destroy()
                os.system('python3 script.py')

            buttonYes = tk.Button (root, text='YES',command=updateYes)
            buttonNo = tk.Button (root, text='NO',command=updateNo)
            buttonYes.pack(pady=10)
            buttonNo.pack()
            root.mainloop()
        else:
            # VERSION EXCEPTION
            print('Something went wrong.')

# EXIT
print('[INFO] Exit.')
