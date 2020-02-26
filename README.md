# DCLV-Monitoring

Because AE is shutting down their web portal Sitelink at the end of March 2020 i was searching about a way how i can monitor my AE/Refusol DCLV PC heater in the future.

Therefor i startet this repo to share my project with all of you who are in the same situation and searchng for an solution.

Steps to do:

1. By the hardware components needed (see ko-fi page)
2. Download Etcher to flash the SD card
    https://www.balena.io/etcher/
3. download Raspbian Lite 
    https://downloads.raspberrypi.org/raspbian_lite_latest
4. Programm Raspbian Lite to SD card with Etcher
5. Copy the (emtpy) ssh file from the repo to the new boot partition
6. Create an Thingspeak account
7. Download the heater.py from this repo
8. Change the ip adress as well as the thingspeak keys in the heater.py file.
9. Optional - change the data entries which are transfered to Thingspeak to your needs
10. Install all needed packages
    sudo apt-get install python-pip
    sudo pip install thingspeak
11. Transfer the file to the Pi Zero
12. Modifying the crontab for calling heater.py every 10 min
    crontab -e
    */10 * * * * python ~/Heater/heater.py

Now you should be able to view your logged data in Thingspeak.
