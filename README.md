# Convert Apple Health export to (Fitbit) CSV

Python scripts to parse your Apple Health data to CSV formats.

* `health_to_fitbit.py` will convert Apple Health data to a FitBit CSV format
* `convert_export-xml_to_csv.py` will convert all Apple Health records to a generic CSV data

For more information, please see the sections below.

## Why

In 2019, I purchased a Garmin smartwatch. Before the watch, I recorded my steps and activity data on my iPhone using Apples Health app. So I needed a way to **import my Apple Health data into Garmin Connect**. However, Garmin connect does not let you import Apple Health data directly.

One solution is to convert the existing Apple Health data to a Fitbit CSV format and then import that into Garmin Connect.

Another solution is to export the data into a generic CSV format and then use these with other programs (such as [GoldenCheetah](https://github.com/GoldenCheetah/GoldenCheetah)).

## Exporting your Apple Health data

To export your Health data from your iPhone, follow these steps:

* Open the Apple Health App on your iPhone
* Click your icon in the top right of the screen
* At the bottom, select "Export All Health Data", confirm with "Export"
* Export the ZIP file via Dropbox / E-Mail / whatever

## health_to_fitbit.py

The `health_to_fitbit.py` script will convert the Apple Health XML files to a FitBit CSV format.

Clone this repository and place both the `export.xml` and the `export_cda.xml` file in the same folder as the Python scripts:

```
$ ll
total 770304
-rw-r--r--@ 1 simon  staff       4839 May  1 15:51 README.md
-rwxr-xr-x@ 1 simon  staff       2318 Apr 10 22:01 convert_export-xml_to_csv.py
-rw-r--r--  1 simon  staff  123884867 May  1 15:49 export.xml
-rw-r--r--  1 simon  staff  261279980 May  1 15:49 export_cda.xml
-rwxr-xr-x  1 simon  staff       3400 Apr 29 20:08 fix_invalid_export_cda_xml.py
-rwxr-xr-x@ 1 simon  staff       4989 May  1 15:41 health_to_fitbit.py
```

Then, execute the script to generate the CSV output:

```
$ ./health_to_fitbit.py
What is your height in cm? 180
OK. Parsing files...
Found weight data for 2016
Found weight data for 2018
Found weight data for 2019
Found weight data for 2020
Found step data for 2015
Found step data for 2017
Now generating FitBit CSV files for the following years: 2016, 2018, 2019, 2020, 2015, 2017
Writing fitbit_2016.csv...
Writing fitbit_2018.csv...
Writing fitbit_2019.csv...
Writing fitbit_2020.csv...
Writing fitbit_2015.csv...
Writing fitbit_2017.csv...
Done.
```

The resulting files will look something like this:

```
Body
Date,Weight,BMI,Fat
"01-01-2019","70.1","0","0"
"02-01-2019","70.1","0","0"
"03-01-2019","70.1","0","0"
[..]

Activities
Date,Calories Burned,Steps,Distance,Floors,Minutes Sedentary,Minutes Lightly Active,Minutes Fairly Active,Minutes Very Active,Activity Calories
"01-01-2019","0","11","0.01","0","0","0","0","0","0"
"02-01-2019","0","13,666","10.4","0","0","0","0","0","0"
"03-01-2019","0","6,901","5.78","0","0","0","0","0","0"
[..]
```

You can now import this data in Garmin Connect by following these steps:

* Log into Garmin Connect, click "Import" in the top right corner
* Click "Browse" and select the generated Fitbit CSV file
* Verify the data format (see above for an example)

If you get an error during import, check that you have selected the correct format for dates and numbers that correspond with the format in the generated CSV.

## convert_export-xml_to_csv.py

The `convert_export-xml_to_csv.py` script can be used to convert your Apple Health data to generic CSV data.
The script exports all records with all fields to CSV.

Place and run the `convert_export-xml_to_csv.py` script in the same folder as your `export.xml` file.
After running the script, the CSV files are available in the same folder (one per Record type in your Apple Health data file):

```
$ ./convert_export-xml_to_csv.py
Start parse.
Finding Record types...
Finding Attributes for HKQuantityTypeIdentifierHeight
Writing HKQuantityTypeIdentifierHeight.csv...

Finding Attributes for HKQuantityTypeIdentifierBodyMass
Writing HKQuantityTypeIdentifierBodyMass.csv...

Finding Attributes for HKQuantityTypeIdentifierHeartRate
Writing HKQuantityTypeIdentifierHeartRate.csv...
[..]
Finding Workouts...
Writing Workouts.csv...
Done.
$ ls -l
-rw-r--r--  1 simon  staff     957665 Apr 10 21:22 HKCategoryTypeIdentifierSleepAnalysis.csv
-rw-r--r--  1 simon  staff     286151 Apr 10 21:22 HKQuantityTypeIdentifierActiveEnergyBurned.csv
-rw-r--r--  1 simon  staff     132679 Apr 10 21:22 HKQuantityTypeIdentifierBasalEnergyBurned.csv
-rw-r--r--  1 simon  staff     113107 Apr 10 21:22 HKQuantityTypeIdentifierBodyMass.csv
-rw-r--r--  1 simon  staff      15226 Apr 10 21:22 HKQuantityTypeIdentifierBodyTemperature.csv
-rw-r--r--  1 simon  staff   26027805 Apr 10 21:22 HKQuantityTypeIdentifierDistanceWalkingRunning.csv
-rw-r--r--  1 simon  staff    9411035 Apr 10 21:22 HKQuantityTypeIdentifierFlightsClimbed.csv
-rw-r--r--  1 simon  staff      40685 Apr 10 21:22 HKQuantityTypeIdentifierHeadphoneAudioExposure.csv
-rw-r--r--  1 simon  staff  120749803 Apr 10 21:22 HKQuantityTypeIdentifierHeartRate.csv
-rw-r--r--  1 simon  staff       1186 Apr 10 21:22 HKQuantityTypeIdentifierHeight.csv
-rw-r--r--  1 simon  staff      26669 Apr 10 21:22 HKQuantityTypeIdentifierRestingHeartRate.csv
-rw-r--r--  1 simon  staff   39502300 Apr 10 21:22 HKQuantityTypeIdentifierStepCount.csv
-rw-r--r--  1 simon  staff      24818 Apr 10 22:02 Workouts.csv
-rwxr-xr-x  1 simon  staff       1112 Apr 10 21:21 convert_export-xml_to_csv.py
-rw-r--r--  1 simon  staff  118092195 Apr  3 10:33 export.xml
```

## Similar or related projects

* [GoldenCheetah/GoldenCheetah](https://github.com/GoldenCheetah/GoldenCheetah)
* [markwk/qs_ledger](https://github.com/markwk/qs_ledger)
* [JohannesHeinrich/garmin-connect-export](https://github.com/JohannesHeinrich/garmin-connect-export)