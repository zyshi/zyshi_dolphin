import sys
from sys import argv
import string
from random import randint
from xlrd import open_workbook

def generatePlot(plot_type, rawxlsfile, visual_filename, x_index_name, y_index_name, x_coln_index, y_coln_index):
	# open the workbook
	wb = open_workbook(rawxlsfile);
	# generated datafile names
	csv_filename = "data" + str(randint(0, 10000)) + ".csv" #TODO: remove later
	tsv_filename = "data"+ str(randint(0, 10000)) + ".tsv"
	period = ','
	tab = "\t"
	# open visual output file 
	visual_output = open(visual_filename, 'w')
	visual_output.truncate()


	if plot_type == "scatter" or plot_type == "bar" or plot_type == "line":
		# processing data
		x_index_name = string.replace(x_index_name, " ", "_")
		y_index_name = string.replace(y_index_name, " ", "_")
		group_index_name = ""
		# if plot_type == "scatter":
		# 	group_index_name = raw_input("Please enter group_index_name: ")
		# 	group_index_name = string.replace(group_index_name, " ", "_")
		# open the output data file: tsv file
		data_output = open(tsv_filename, 'w')
		data_output.truncate()

		lineCnt = 0;
		for s in wb.sheets():
			for row in range(s.nrows):
				x_val = str(s.cell(row, x_coln_index));
				y_val = str(s.cell(row, y_coln_index));
				if (not "empty" in x_val) and (not "empty" in y_val) : 
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
		group_index_name = string.replace(x_index_name, " ", "_")
		value_index_name = string.replace(y_index_name, " ", "_")
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

def isNumber(s):
    try:
        float(s)
        return True                
    except:
        return False

# eror checking of the usage
if len(argv) != 2:
	print "================================================================================="
	print "== Error: Wrong usage of command line arguments                                =="
	print "== Usage: python <script.py> [xls_filename]                                    =="
	print "================================================================================="
	sys.exit(-1);

# open the workbook
wb = open_workbook(argv[1])

for s in wb.sheets():
	cnt = 0;
	for col1 in range(s.ncols):
		x_is_number = True
		x_is_string = True
		y_is_number = True
		x_is_string = True
		# escape the blank space to _
		x_index_name = string.replace(str(s.cell(0, col1).value), " ", "_")
		# check whether all x_val is number 
		for itr in range(s.nrows):
			if itr > 0:
				x_val = string.replace(str(s.cell(itr, col1).value), " ", "")
				if x_val != "":
					if isNumber(x_val):
						x_is_string = False
					else: # x is string
						x_is_number = False

		for col2 in range(s.ncols):
			if col2 > col1:
				cnt += 1
				y_index_name = string.replace(str(s.cell(0, col2).value), " ", "_")
				# check whether all y_val is number
				for itr in range(s.nrows):
					if itr > 0:
						y_val = string.replace(str(s.cell(itr, col2).value), " ", "")
						if y_val != "":
							if isNumber(y_val):
								y_is_string = False
							else:
								y_is_number = False

				if x_is_number and y_is_number :
					output1 = "scatterplot_x" + str(col1) + "_y" + str(col2) + ".html"
					# output2 = "scatterplot_x" + str(col2) + "_y" + str(col1) + ".html"
					generatePlot("scatter", argv[1], output1, x_index_name, y_index_name, col1, col2)
					# generatePlot("scatter", argv[1], output2, y_index_name, x_index_name)
				elif x_is_number and y_is_string:
					output = "barplot_x" + str(col2) + "_y" + str(col1) + ".html"
					generatePlot("bar", argv[1], output, y_index_name, x_index_name, col2, col1)
				elif x_is_string and y_is_number:
					output = "barplot_x" + str(col1) + "_y" + str(col2) + ".html"
					generatePlot("bar", argv[1], output, x_index_name, y_index_name, col1, col2)
				else:
					print "ignoring the output"