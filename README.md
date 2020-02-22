# DCLV-Monitoring

Because AE is shutting down their web portal Sitelink at the end of March 2020 i was searching about a way how i can monitor my AE/Refusol DCLV PC heater in the future.

Therefor i startet this repo to share my project with all of you who are in the same situation and searchng for an solution.

Steps to do:

1. By the hardware components needed (see ko-fi page)
2. Create an Thingspeak account
3. Download the heater.py from this repo
4. Change the ip adress as well as the thingspeak keys in the heater.py file.
5. (Optional - change the data entries which are transfered to Thingspeak to your needs)
6. Transfer the file to the Pi Zero
7. Modifying the crontab for calling heater.py every 10 min.

Now you should be able to view your logged data in Thingspeak.
