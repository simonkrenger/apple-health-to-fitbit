#!/usr/bin/env python3

# Script to convert Apple Health data to Fitbit CSV data

import os.path
import xml.etree.ElementTree as ET

from datetime import datetime

if not os.path.exists('export_cda.xml'):
  print("Error: export_cda.xml not found.")
  exit(1)

if not os.path.exists('export.xml'):
  print("Error: export.xml not found.")
  exit(1)

height_cm_input = input("What is your height in cm? ")
try:
	height_cm = int(height_cm_input)
	height_m = float(height_cm) / 100.0
except:
	print("Unable to parse input.")
	exit(1)

print("OK. Parsing files...")

try:
  export_cda = ET.parse('export_cda.xml')
except ET.ParseError as error:
	print("Unable to parse 'export_cda.xml', it might be invalid XML.")
	print("Try to fix 'export_cda.xml' by running the included 'fix_invalid_export_cda_xml' script.")
	print("Exiting")
	exit(1)

try:
	export = ET.parse('export.xml')
except ET.ParseError as error:
	print("Failed to parse 'export.xml'.")
	print("Exiting")
	exit(1)


export_cda_root = export_cda.getroot()
export_root = export.getroot()

# Go through export_cda.xml to get all weight values

weight_dict = {}

for entry in export_cda_root.findall('{urn:hl7-org:v3}entry'):
	for organizer in entry.findall('{urn:hl7-org:v3}organizer'):
		for component in organizer.findall('{urn:hl7-org:v3}component'):
			observation = component.find('{urn:hl7-org:v3}observation')
			
			code = observation.find('{urn:hl7-org:v3}code').get('code')
			if(code == "3141-9"):
				value = observation.find('{urn:hl7-org:v3}value').get('value')
				effective_time = observation.find('{urn:hl7-org:v3}effectiveTime').find('{urn:hl7-org:v3}low')
				time_value = datetime.strptime(effective_time.get('value'), '%Y%m%d%H%M%S%z')
				date_string = time_value.strftime('%d-%m-%Y')

				weight_dict[date_string] = value

# Go through export.xml to get all activities, steps, distance, floors climbed

steps_dict = {}
distance_dict = {}
floors_dict = {} 

for record in export_root.findall('Record'):
	start_date = datetime.strptime(record.get('startDate'), '%Y-%m-%d %H:%M:%S %z')
	date_string = start_date.strftime('%d-%m-%Y')
	value = record.get('value')

	# Aggregate the data by calculating the sum for each date
	if(record.get('type') == "HKQuantityTypeIdentifierStepCount"):
		if date_string in steps_dict:
			steps_dict[date_string] = int(steps_dict[date_string]) + int(value)
		else:
			steps_dict[date_string] = int(value)

	if(record.get('type') == "HKQuantityTypeIdentifierDistanceWalkingRunning"):
		if date_string in distance_dict:
			distance_dict[date_string] = float(distance_dict[date_string]) + float(value)
		else:
			distance_dict[date_string] = float(value)

	if(record.get('type') == "HKQuantityTypeIdentifierFlightsClimbed"):
		if date_string in floors_dict:
			floors_dict[date_string] = int(floors_dict[date_string]) + float(value)
		else:
			floors_dict[date_string] = float(float(value))

# Find out which years we need to print
# All dict keys are formated with "time_value.strftime('%d-%m-%Y')"
years = []

for date_key in weight_dict:
	tmp_year = datetime.strptime(date_key, '%d-%m-%Y').strftime('%Y')
	if tmp_year not in years:
		print("Found weight data for " + tmp_year)
		years.append(tmp_year)

for date_key in steps_dict:
	tmp_year = datetime.strptime(date_key, '%d-%m-%Y').strftime('%Y')
	if tmp_year not in years:
		print("Found step data for " + tmp_year)
		years.append(tmp_year)

print("Now generating FitBit CSV files for the following years: " + ', '.join(years))

for file_year in years:
	filename = "fitbit_" + file_year + ".csv"
	print("Writing " + filename + "...")
	with open(filename, 'w') as output_file:

	  # Print weight

		# Header
		output_file.write("Body\n")
		output_file.write("Date,Weight,BMI,Fat\n")

		# Data
		for date_key in weight_dict:
			dict_year = datetime.strptime(date_key, '%d-%m-%Y').strftime('%Y')
			if(dict_year == file_year):
				value = weight_dict[date_key]
				bmi = round(float(value) / (height_m * height_m),2)
				output_file.write("\"%s\",\"%s\",\"%s\",\"0\"\n" % (date_key, value, bmi))

		# Print activities

		# Header
		output_file.write("\n")
		output_file.write("Activities\n")
		output_file.write("Date,Calories Burned,Steps,Distance,Floors,Minutes Sedentary,Minutes Lightly Active,Minutes Fairly Active,Minutes Very Active,Activity Calories\n")

		# Data
		for date_key in steps_dict:
			dict_year = datetime.strptime(date_key, '%d-%m-%Y').strftime('%Y')
			if(dict_year == file_year):
				output = "\""
				output += date_key
				output += "\",\"0\",\""

				if date_key in steps_dict:
					output += str("{:,}".format(steps_dict[date_key]))
			    
				output += "\",\""

				if date_key in distance_dict:
					output += str(round(distance_dict[date_key],2))
				else:
					output += "0"

				output += "\",\""

				if date_key in floors_dict:
					output += str(floors_dict[date_key])
				else:
					output += "0"

				output += "\",\"0\",\"0\",\"0\",\"0\",\"0\"\n"

				output_file.write(output)

print("Done.")
