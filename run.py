4

### MODULES ###
try:
    import urllib.request
    import os.path
    import sys
    import tkinter as tk
except ModuleNotFoundError as err:
    print('[ERROR] ', err, '. Install required module with "pip" command first (e.g. python3 -m pip install <module>).')
    input('Press any key to continue...')
    exit()

### WEBPAGE ###
urlscript = 'https://raw.githubusercontent.com/geludwig/DreamGuardAndDatagrabber/main/script.py'

### CATCH macOS EXCEPTIONS ###
if sys.platform == 'darwin':
    print(sys.platform)
    print('[WARNING] System runs macOS. Errors may occur due to platform limitations.')
    input('Press any key to continue...')
    try:
        urllib.request.urlopen(urlscript)
    except:
        print('[ERROR] URL ERROR: May need to install CA certificates first.')


### GET PYTHON PATH ###
pathpython = str(sys.executable)
script = 'script.py'
shell = pathpython+' '+script
 
### DOWNLOAD SCRIPT ###
# NO SCRIPT IN DIR
if (os.path.exists('script.py') is False):
    print('[INFO] Fetching script.py.')
    try:
        urllib.request.urlretrieve(urlscript, filename='script.py')
        os.system(shell)
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
        os.system(shell)
        exit()
    except urllib.error.URLError as e:
        print('[ERROR] URL error: ', e)
        print('[WARNING] Can not verify version, fallback to local file.')
        os.system(shell)
        exit()

    # GET SCRIPT VERSION
    with open('script.py', "r") as file:
        versionscript = int(file.readline().strip())
        if versionweb == versionscript:
            # VERSION MATCH, NOTHING TO DO
            print('[INFO] All files up to date.')
            os.system(shell)
            exit()

        # NEW VERSION AVAILABLE, root DIALOG, DOWNLOAD NEW SCRIPT
        elif versionweb > versionscript:
            def rootYes():
                root.destroy()
                try:
                    print('[INFO] Updating python script.')
                    urllib.request.urlretrieve(urlscript, filename='script.py')
                    os.system(shell)
                    exit()
                except urllib.error.HTTPError as e:
                    print('[ERROR] HTTP error: ', e)
                    exit()
                except urllib.error.URLError as e:
                    print('[ERROR] URL error: ', e)
                    exit()

            def rootNo():
                root.destroy()
                os.system(shell)
                exit()

            print('[INFO] New version available.')
            root = tk.Tk()
            root.geometry('300x100')
            root.resizable(False, False)
            root.title('root SCRIPT?')
            buttonYes = tk.Button (root, text='YES',command=rootYes)
            buttonNo = tk.Button (root, text='NO',command=rootNo)
            buttonYes.pack(pady=10)
            buttonNo.pack()
            root.mainloop()

        # VERSION EXCEPTION
        else:
            print('Something went wrong.')
