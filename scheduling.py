#!/usr/bin/python3
# This ^ needs to be portable. Maybe a binary would be easier than python? I suspect this program will be run on Windows and MacOS and the less setup the better.

# Step 1: Unzip the results
# TODO: Get the filename from the command line? Just search for a .zip file in the directory?
# Source: https://stackoverflow.com/questions/3451111/unzipping-files-in-python
import zipfile
with zipfile.ZipFile("Mentor Scheduling Form.csv.zip","r") as zip_ref:
	zip_ref.extractall(".")

# Step 2: Read resulting csv file
# Source: https://realpython.com/python-csv/
import csv
with open("Mentor Scheduling Form.csv") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			print(f'Column names are {", ".join(row)}')
			line_count += 1
		else:
			print(f'\n{row[0]};\t {row[1]};\t {row[2]};\t {row[3]};\t {row[4]}')
			line_count += 1
	print(f'Processed {line_count} lines.')
