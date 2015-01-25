import sys
from sys import argv
import string
from random import randint
from xlrd import open_workbook

# eror checking of the usage
if len(argv) != 4:
	print "================================================================================="
	print "== Error: Wrong usage of command line arguments                                =="
	print "== Usage: python <script.py> [xls_filename] [visual_output.html] [plot_type]   =="
	print "== Plot_type: scatter, bar, line,                                              =="
	print "==        follow the exact order of the arguments                              =="
	print "================================================================================="
	sys.exit(-1);

# open the workbook
wb = open_workbook(argv[1])

plot_type = argv[3]
if plot_type != "scatter" and plot_type != "bar" and plot_type != "line" and plot_type != "pie":
	print "================================================================================="
	print "== Error: Wrong plot type                                					  =="
	print "== Plot_type: scatter, bar, line, pie                                          =="
	print "================================================================================="

# generated datafile names
csv_filename = "data" + str(randint(0, 100)) + ".csv"
tsv_filename = "data"+ str(randint(0, 100)) + ".tsv"
period = ','
tab = "\t"

# open visual output file 
visual_filename = argv[2]
visual_output = open(visual_filename, 'w')
visual_output.truncate()

if plot_type == "scatter" or plot_type == "bar" or plot_type == "line":
	# processing data
	# can change the user input to command line input if needed
	x_index_name = raw_input("Please enter x_index_name: ")
	y_index_name = raw_input("Please enter y_index_name: ")
	group_index_name = ""
	if plot_type == "scatter":
		group_index_name = raw_input("Please enter group_index_name: ")
		group_index_name = string.replace(group_index_name, " ", "")

	# open the output data file: tsv file
	data_output = open(tsv_filename, 'w')
	data_output.truncate()

	# navigate the work sheet
	# ===========================
	# = xinput, yinput, (group) =
	# ===========================
	lineCnt = 0;
	for s in wb.sheets():
		for row in range(s.nrows):
			new_line = ""
			for col in range(s.ncols):
				# escape the blank space to _
				word = string.replace(str(s.cell(row, col).value), " ", "_")
				new_line += word
				new_line += tab
			if lineCnt == 0:
				# processing the first line of data file
				new_line = string.replace(new_line, x_index_name, "xinput")
				new_line = string.replace(new_line, y_index_name, "yinput")
				if plot_type == "scatter" and group_index_name != "":
						new_line = string.replace(new_line, group_index_name, "group")			
				lineCnt += 1
			if new_line != "":
				data_output.write(new_line)
				data_output.write("\n")
	# close the file
	data_output.close()

	# sort if it's line chart TODO
else:
	# pie chart change to tsv TODO
	# processing data
	# can change the user input to command line input if needed
	group_index_name = raw_input("Please enter group_index_name: ")
	value_index_name = raw_input("Please enter value_index_name: ")

	# open the output data file: tsv file
	data_output = open(csv_filename, 'w')
	data_output.truncate()

	lineCnt = 0;
	for s in wb.sheets():
		for row in range(s.nrows):
			new_line = ""
			for col in range(s.ncols):
				# remove blank space in the same cell
				word = string.replace(str(s.cell(row, col).value), " ", "")
				new_line += word
				new_line += period
			if lineCnt == 0:
				# processing the first line of data file
				new_line = string.replace(new_line, group_index_name, "group")
				new_line = string.replace(new_line, value_index_name, "values")		
				lineCnt += 1
			if new_line != "":
				data_output.write(new_line)
				data_output.write("\n")
	# close the file
	data_output.close()


# writing html file
if plot_type == "scatter":
	templateFile = "scatter_template.html"
elif plot_type == "bar":
	templateFile = "bar_template.html"
elif plot_type == "line":
	templateFile = "line_template.html"
else:
	templateFile = "pie_template.html"

yLabel_found = 0
xLabel_found = 0
datafile_found = 0

with open(templateFile) as file:
	for line in file:
		if "dataInputFile" in line and datafile_found == 0:
			datafile_found += 1
			if plot_type == "pie":
				line = "var dataInputFile = \"" + str(csv_filename)+ "\";\n"
			else:				
				line = "var dataInputFile = \"" + str(tsv_filename)+ "\";\n"
		elif "yLabel" in line and yLabel_found == 0: 
			yLabel_found += 1
			# modify yLabel
			line = "var yLabel = \"" + str(y_index_name) + "\";\n"  
		elif "xLabel" in line and xLabel_found == 0:
			xLabel_found += 1
			# modify xLabel
			line = "var xLabel = \"" + str(x_index_name) + "\";\n"  
		visual_output.write(line)
visual_output.close()