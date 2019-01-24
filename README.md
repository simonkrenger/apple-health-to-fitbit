# Convert Apple Health export to Fitbit CSV

A Python script to convert an Apple Health XML export to a Fitbit CSV file.

## Why

I recently purchased a new Garmin smartwatch. Before the watch, I recorded my steps and activity data on my iPhone using Apples Health app. So I needed a way to **import my Apple Health data into Garmin Connect**. However, Garmin connect does not let you import Apple Health data directly.

The solution was to convert the existing Apple Health data to a Fitbit CSV format and then import that into Garmin Connect.

The script will convert the following data:

* Weight
* Steps
* Floors climbed

## Usage

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
