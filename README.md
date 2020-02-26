# DCLV-Monitoring

Because AE is shutting down their web portal Sitelink at the end of March 2020 i was searching about a way how i can monitor my AE/Refusol DCLV PC heater in the future.

Therefor i startet this repo to share my project with all of you who are in the same situation and searchng for an solution.

Steps to do:

1. By the hardware components needed (see ko-fi page)
2. Download Etcher to flash the SD card
    https://www.balena.io/etcher/
3. Download Raspbian Lite 
    https://downloads.raspberrypi.org/raspbian_lite_latest
4. Programm Raspbian Lite to SD card with Etcher
5. Creating an (empty) ssh file on Windows via 
```
STRG+R
cmd
copy con ssh
STRG+Z
Enter
```
6. Copy the ssh file to boot partition of SD card
7. Create an Thingspeak account
    https://thingspeak.com/
8. Download the heater.py from this repo
9. Change the ip adress as well as the thingspeak keys in the heater.py file. You find it under your Thingsspeak channel - Settings
10. Optional - change the data entries which are transfered to Thingspeak to your needs
11. Install all needed packages
```
    sudo apt-get install python-pip
    sudo pip install thingspeak
```
12. Transfer the file to the Pi Zero
13. Modifying the crontab for calling heater.py every 10 min
```   
   crontab -e
    */10 * * * * python ~/Heater/heater.py
```
Now you should be able to view your logged data in Thingspeak.
