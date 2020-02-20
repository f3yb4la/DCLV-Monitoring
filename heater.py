#!/usr/bin/env python3
import ftplib
import struct
import thingspeak
import time
from datetime import date
import os
import datetime
import socket



def main():
	hostname = "192.168.178.99"
	ftp_user = "refu"
	ftp_password = "EE0129"
	channel_id = 982813 # PUT YOUR ID HERE
	write_key = 'KEAFAOM9W6HN2W2D' #PUT YOUR WRITE KEY HERE
	read_key = 'EHWDQNNSHIYJJ10F' #PUT YOUR READ KEY HERE	
	dataset_length = 10
	additional_header_length = 18
	amount_of_datasets = 18
	size_of_dataset_header = 6
	size_of_dataset_info = 4

	#determine actual date

	actual_date = date.today()
	
	s_year = str(actual_date.year)
	#print(s_year)
	
	if actual_date.month<10 :
		s_month = "0" + str(actual_date.month)
	else: s_month = str(actual_date.month)
	
	if actual_date.day<10 :
		s_day = "0" + str(actual_date.day)
	else: s_day = str(actual_date.day)
	
	# creating all directories for the complete year
	
	akt_path=os.getcwd()
	try:
		os.mkdir(s_year)
	except OSError:
		print ("Creation of the directory %s failed maybe already existing" % s_year)
	else:
		print ("Successfully created the directory")
	
	os.chdir(s_year)
	for i in range (1,13):
		if i < 10:
			dir_name = "0"+ str(i)
			try:
				os.mkdir(dir_name)
			except OSError:
				print ("Creation of the directory failed: %s maybe already existing" % dir_name)
			else:
				print ("Successfully created the directory: %s" % dir_name)
			
		else:
			dir_name = str(i)
			try:
				os.mkdir(dir_name)
			except OSError:
				print ("Creation of the directory failed: %s maybe already existing" % dir_name)
			else:
				print ("Successfully created the directory: %s" % dir_name)
			
		
	
	os.chdir(s_month)
	
	#open local temporary file
	print("Open temp file for writing")
	temp_file_name = "temp.log"
	temp_file = open(temp_file_name, 'wb')
	
	#doing the FTP stuff
	print("Open connection to FTP Server")
	try: 
		ftp = ftplib.FTP(hostname, ftp_user, ftp_password, timeout=10)
	except ftplib.all_errors:
		print("FTP Server not reachable aborting connection")
		
		print("Close temp file")
		temp_file.close()
		print("Deleting temporary file")
		if os.path.exists(temp_file_name):
			os.remove(temp_file_name)
			print("Successful")
		else:
			print("Failed")
   
	else:
		# higher debug level not needed anymore
		#ftp.set_debuglevel(2)
		ftp.set_pasv(False)
		remote_path = "/data/logger/"+s_year+"/"+s_month
		ftp.cwd(remote_path)
		retr_command = "RETR "+s_day+".log"
		print("Get file from FTP")
		ftp.retrbinary(retr_command, temp_file.write)
		print("Closing FTP connection")
		ftp.close()
		
		# Determine the file length of the received file
		print("Move to the end of the received file to get length")
		temp_file.seek(0,2)
		temp_file_size = temp_file.tell()
		print("Length of temporary file %d" % temp_file_size)
		print("Close temp file...")
		temp_file.close()
		print("Open temp file for reading")
		temp_file = open("temp.log", 'rb')	
		
		#open local logfile
		local_filename = s_day +".log"
		print("Filename for the local file: " + local_filename)
		print("Trying to open local logfile")
		
		try:
			local_file = open(local_filename, 'rb')
		except IOError:
			print("Error - no logfile existing")
			print("Creating an new file")
			local_file = open(local_filename, 'wb')
			print("closing the local file")
			local_filesize=0;
		else:
			# get bytecount of local logfile
			# move to the end of the file
			print("Move to end to get filesize")
			local_file.seek(0,2)
			# get the position in bytes
			local_filesize=local_file.tell()
			print("Length of old, stored local file %d" % local_filesize)
			print("Closing local file...")	
		
		local_file.close()
		
		print("Open local file for writing or creating new one")
		local_file = open(local_filename, 'wb')
		
		
		
		
		#storage for 18 values, maybe easier to allocate
		myValue = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		
		# offset consisting of 18 datasets with 10 byte each + 12 byte 0xFF + 4 byte Unix time + 2 bytes length information
		offset = amount_of_datasets*dataset_length + additional_header_length
		
		if temp_file_size > local_filesize:
			# newer data was on ftp server - copy to logal logfile
			print("More data in received file than in local file")
			print("Transfer data from received file to local file")
			print("Transfer data from received file to old logfile")
			local_file.write(temp_file.read())
			print("Closing local file...")
			local_file.close()
			print("Open local file for reading...")
			local_file = open(local_filename, 'rb')
			# move to the start of the last entry
			local_file.seek(-offset,2)
			
			unixtime=local_file.read(4)
			trennzeichen=local_file.read(14)
			
			timeint=struct.unpack('>I', unixtime)
			print(timeint)

			print(datetime.datetime.fromtimestamp(int(timeint[0])).strftime('%Y-%m-%d %H:%M:%S'))

			for i in range (0,amount_of_datasets):
				
				headerData = local_file.read(size_of_dataset_header)
				tagData = local_file.read(size_of_dataset_info)
				# Endian format change with >
				newval = struct.unpack('>f', tagData)
				#newval is a tuple with float as first element
				myValue[i]=newval[0]
				# value printing moved to point after renaming it
				print("%.2f" % newval)
			
			enable_transmission=1;
		else:
			print("No new data available")
			enable_transmission=0;
			
				
		
		print("Reading of datablocks from local file complete")
		print("Closing both local and temporary file")
		# closeing all files
		temp_file.close()
		local_file.close()
		
		# Deleting the temporary file from filesystem

		print("Deleting temporary file")
		if os.path.exists(temp_file_name):
			os.remove(temp_file_name)
			print("Successful")
		else:
			print("Failed")
		
		# giving new names
		dc_power1 = round(myValue[0],2)
		dc_power2 = round(myValue[1],2)
		dc_power3 = round(myValue[2],2)
		ww_temp = round(myValue[4],2)
		int_temp = round(myValue[5],2)
		dc_voltage1 = round(myValue[9],2)
		dc_voltage2 = round(myValue[10],2)
		dc_voltage3 = round(myValue[11],2)
		total_kWh = round((myValue[12]/10),2)
		kWh_gen1 = round((myValue[13]/10),2)
		kWh_gen2 = round((myValue[14]/10),2)
		kWh_gen3 = round((myValue[15]/10),2)
		#kWh_day	 = round((myValue[16]/10),2)
		kWh_day = round((kWh_gen1+kWh_gen2+kWh_gen3),2)
		akt_power = round((dc_power1+dc_power2+dc_power3),2)
		
		print("DC Power total: %f" % akt_power)
		print("Water Temp %f" % ww_temp)
		print("Total kWh %f" % total_kWh)
		print("Actual Day kWh: %f" % kWh_day)
		print("Internal Temperature: %f" % int_temp)
		print("DC Power 1: %f" % dc_power1)
		print("DC Power 2: %f" % dc_power2)
		print("DC Power 3: %f" % dc_power3)	
		
		
		# sending data to thingspeak
		
		if enable_transmission:
			
			print("Sending data to thingspeak")
			channel = thingspeak.Channel(channel_id, write_key, read_key)
			try:
				# write
				response = channel.update({	'field1': akt_power, 	'field2': ww_temp, 
											'field3': total_kWh, 	'field4': kWh_day, 
											'field5': int_temp, 	'field6': dc_power1, 
											'field7': dc_power2, 	'field8': dc_power3})
			
				print("Sending of data completed")	
			except:
				print("connection failed")
			
			
		else:
			print("No new data to send")
		
	print("Python script complete")
				


if __name__ == "__main__":
    main()