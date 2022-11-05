# DraegerDreamguard

Dreamguard was a product released by Draeger to monitor the respiration of infants. The product was discontinued on 31.12.2021. The following scripts were written for the prototype version, which were used for a PhD thesis.

https://www.draeger.com/Library/Content/dreamguard-gebrauchsanweisung.pdf (retrieved 20.05.2022)

sensor.py : Used to transfer data via serial interface from sensor to hex file.

diagram.py : Convert sensor data and datagrabber data (Draeger Monitoring Tool for Infinity Devices) to diagram via matplot.

calcminmax.py : search min/max/median/average values of a particular measurement.
