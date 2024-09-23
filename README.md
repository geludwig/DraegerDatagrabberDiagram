# DraegerDreamguard

Dreamguard was a product released by Draeger to monitor the respiration of infants. The product was discontinued on 31.12.2021. This phython scripts was written for the prototype version, which was used for a PhD thesis. The script compares the data from the Dreamguard sensor with the EKG data, sets the correct timeline and offsets and displays it via an interactive diagram.

## How to install
1) Download Python from https://www.python.org/downloads/
2) Install Python and check "Add to PATH" during installation.
3) Download script via https://github.com/geludwig/DraegerDreamGuard/releases/latest

## How to use
1) Run "_main.py" (script may install missing modules itself)
2) Choose the corresponding CSV and TXT files (2 examples, both including Back and Prone position, are included in the folder "input_files")
3) You can click on "acc x", "acc y", ... in the legend of the lower plot to enable/disable the corresponding graphs (zoom and move tool must be disabled)

## Files
- CSV : Recorded files from "Draeger Datagrabber" via EKG leads
- TXT : Recorded files from prototype sensor installed on infant

## Sensor data
- Sensor file contains hex values which get imported in "dreamguard_import.py" (look there for the definition of each column).
- Imported hex values are converted in "dreamguard_sensor.py" to their corresponding decimal values.
