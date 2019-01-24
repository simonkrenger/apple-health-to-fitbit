#!/usr/bin/env python3

from datetime import datetime

import xml.etree.ElementTree as ET

export_cda = ET.parse('export_cda.xml')
export_cda_root = export_cda.getroot()

export = ET.parse('export.xml')
export_root = export.getroot()

print("Body")
print("Date,Weight,BMI,Fat")

for entry in export_cda_root.findall('{urn:hl7-org:v3}entry'):
	for organizer in entry.findall('{urn:hl7-org:v3}organizer'):
		for component in organizer.findall('{urn:hl7-org:v3}component'):
			observation = component.find('{urn:hl7-org:v3}observation')
			
			code = observation.find('{urn:hl7-org:v3}code').get('code')
			value = observation.find('{urn:hl7-org:v3}value').get('value')

			effective_time = observation.find('{urn:hl7-org:v3}effectiveTime').find('{urn:hl7-org:v3}low')
			time_value = datetime.strptime(effective_time.get('value'), '%Y%m%d%H%M%S%z')
			date_string = time_value.strftime('%d-%m-%Y')

			if(code == "3141-9"):
				# Use the following two lines to also calculate BMI as well (1.80 = height in m)
        		#bmi = round(float(value) / (1.80 * 1.80),2)
				#print("\"%s\",\"%s\",\"%s\",\"0\"" % (date_string, value, bmi))
        		print("\"%s\",\"%s\",\"0\",\"0\"" % (date_string, value))

print("")
print("Activities")
print("Date,Calories Burned,Steps,Distance,Floors,Minutes Sedentary,Minutes Lightly Active,Minutes Fairly Active,Minutes Very Active,Activity Calories")

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
			floors_dict[date_string] = int(floors_dict[date_string]) + int(value)
		else:
			floors_dict[date_string] = int(value)

# Iterate over all dates we found
for date_key in steps_dict:
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

	output += "\",\"0\",\"0\",\"0\",\"0\",\"0\""

	print(output)
