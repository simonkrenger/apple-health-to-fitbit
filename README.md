# Convert Apple Health export to (Fitbit) CSV

A Python script to convert an Apple Health XML export to a Fitbit CSV file.
There is also a script to generate a generic CSV file from your Apple Health data.

## Why

I recently purchased a new Garmin smartwatch. Before the watch, I recorded my steps and activity data on my iPhone using Apples Health app. So I needed a way to **import my Apple Health data into Garmin Connect**. However, Garmin connect does not let you import Apple Health data directly.

The solution was to convert the existing Apple Health data to a Fitbit CSV format and then import that into Garmin Connect.

The script will convert the following data:

* Weight
* Steps
* Floors climbed

Everything else is ignored (for example sleep data). Feel free to modify the script to include this data as well.

There is also a script to convert the Apple Health data into generic CSV.

## Usage (health_to_fitbit.py)

Create an Apple Health export on your iPhone and extract the archive. Clone the repository and place both the `export.xml` and the `export_cda.xml` file in the same folder as the Python script:

```
$ ls -l
total 85272
-rw-r--r--@ 1 simon  staff  43414634 Jan 21 22:49 export.xml
-rw-r--r--@ 1 simon  staff    232341 Jan 21 22:49 export_cda.xml
-rwxr-xr-x@ 1 simon  staff      2642 Jan 22 20:53 health_to_fitbit.py
```

Then, execute the script to generate the CSV output:

```
$ ./health_to_fitbit.py > fitbit_format.csv
```

The resulting file will look something like this:

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

## How to import the data in Garmin Connect

* Log into Garmin Connect, click "Import" in the top right corner
* Click "Browse" and select the generated Fitbit CSV file
* Verify the data format (see above for an example)

If you get an error during import, check the following:

* Garmin Connect only allows uploading values for one year. If you have multiple years of data, manually edit the file to make sure the CSV only contains one year at a time (e.g. only 2017).
* Check that you have selected the correct format for dates and numbers that correspond with the format in the generated CSV.

## Usage (convert_export-xml_to_csv.py)

Place and run the `convert_export-xml_to_csv.py` script in the same folder as your `export.xml` file.
After running the script, the CSV files are available in the same folder (one per Record type):

```
$ ./convert_export-xml_to_csv.py
[..]
$ ls -l
-rw-r--r--@ 1 simon  staff     957665 Apr 10 21:22 HKCategoryTypeIdentifierSleepAnalysis.csv
-rw-r--r--  1 simon  staff     286151 Apr 10 21:22 HKQuantityTypeIdentifierActiveEnergyBurned.csv
-rw-r--r--  1 simon  staff     132679 Apr 10 21:22 HKQuantityTypeIdentifierBasalEnergyBurned.csv
-rw-r--r--  1 simon  staff     113107 Apr 10 21:22 HKQuantityTypeIdentifierBodyMass.csv
-rw-r--r--  1 simon  staff      15226 Apr 10 21:22 HKQuantityTypeIdentifierBodyTemperature.csv
-rw-r--r--  1 simon  staff   26027805 Apr 10 21:22 HKQuantityTypeIdentifierDistanceWalkingRunning.csv
-rw-r--r--@ 1 simon  staff    9411035 Apr 10 21:22 HKQuantityTypeIdentifierFlightsClimbed.csv
-rw-r--r--  1 simon  staff      40685 Apr 10 21:22 HKQuantityTypeIdentifierHeadphoneAudioExposure.csv
-rw-r--r--  1 simon  staff  120749803 Apr 10 21:22 HKQuantityTypeIdentifierHeartRate.csv
-rw-r--r--  1 simon  staff       1186 Apr 10 21:22 HKQuantityTypeIdentifierHeight.csv
-rw-r--r--  1 simon  staff      26669 Apr 10 21:22 HKQuantityTypeIdentifierRestingHeartRate.csv
-rw-r--r--  1 simon  staff   39502300 Apr 10 21:22 HKQuantityTypeIdentifierStepCount.csv
-rw-r--r--@ 1 simon  staff      24818 Apr 10 22:02 Workouts.csv
-rwxr-xr-x  1 simon  staff       1112 Apr 10 21:21 convert_export-xml_to_csv.py
-rw-r--r--@ 1 simon  staff  118092195 Apr  3 10:33 export.xml
```
