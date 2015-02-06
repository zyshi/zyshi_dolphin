import sys
from sys import argv
import string
import os
from random import randint
from xlrd import open_workbook
from util import __SAVE_DATA_DIR
from util import __SAVE_JS_DIR
from util import __SAVE_CSV_DIR
# from util import __SAVE_OUTPUT_DIR
from util import __TEMP_DIR

def generatePlot(plot_type, rawxlsfile, visual_filename, x_index_name, y_index_name, x_coln_index, y_coln_index, datadirectory):
	tagid = "x" + str(x_coln_index) + "y" + str(y_coln_index)
	chartid = "chart" + tagid
	# open the workbook
	wb = open_workbook(rawxlsfile);
	# generated datafile names
	csv_filename = datadirectory + "/" + "data" + str(randint(0, 10000)) + ".csv" #TODO: remove later
	tsv_filename =  datadirectory + "/" + "data"+ str(randint(0, 10000)) + ".tsv"
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
					if row == 0:
						new_line = "xinput" + tab + "yinput"
					else:
						new_line = ""
						word = string.replace(str(s.cell(row, x_coln_index).value), " ", "_")
						new_line += word
						new_line += tab
						word = string.replace(str(s.cell(row, y_coln_index).value), " ", "_")
						new_line += word
						new_line += tab
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

	# writing js files
	if plot_type == "scatter":
		templateFile = __SAVE_JS_DIR + "/scatter_temp.js"
	elif plot_type == "bar":
		templateFile = __SAVE_JS_DIR +"/bar_temp.js"
	elif plot_type == "line":
		templateFile = __SAVE_JS_DIR +"/line_temp.js"
	else:
		templateFile = __SAVE_JS_DIR +"/pie_temp.js"

	yLabel_found = 0
	xLabel_found = 0
	datafile_found = 0
	newYlabel = "yLabel" + tagid
	newXlabel = "xLabel" + tagid

	with open(templateFile) as file:
		for line in file:
			if "tagid" in line:
				line = string.replace(line, 'tagid', tagid)

			if "dataInputFile" in line and datafile_found == 0:
				datafile_found += 1
				if plot_type == "pie":
					line = "var dataInputFile = \"" + str(csv_filename)+ "\";\n"
				else:				
					line = "var dataInputFile = \"" + str(tsv_filename)+ "\";\n"
			elif "yLabel" in line:
				if yLabel_found == 0: 
					yLabel_found += 1
					# modify yLabel
					line = "var yLabel = \"" + str(y_index_name) + "\";\n"
				line = string.replace(line, "yLabel", newYlabel)
			elif "xLabel" in line: 
				if xLabel_found == 0:
					xLabel_found += 1
					# modify xLabel
					line = "var xLabel = \"" + str(x_index_name) + "\";\n" 
				line = string.replace(line, "xLabel", newXlabel)
			elif "chart" in line:
				line = string.replace(line, "chart", chartid)
			visual_output.write(line)
	visual_output.close()

def isNumber(s):
    try:
        float(s)
        return True                
    except:
        return False


def autoplotGenerator(fname):
	# load the xls file path
	rawxlsfile = __SAVE_CSV_DIR + "/" + fname

	# create a separate js folder to store ds js files for this data
	jsdirectory = __SAVE_JS_DIR + "/graph_js/" + string.replace(fname,".xls", "");
	if not os.path.exists(jsdirectory):
		os.makedirs(jsdirectory)

	# create a separate datas folder to store ds js files for this data
	datadirectory = __SAVE_DATA_DIR + "/" + string.replace(fname,".xls", "");
	print datadirectory
	if not os.path.exists(datadirectory):
		os.makedirs(datadirectory)

	# open the workbook
	wb = open_workbook(rawxlsfile)

	# open result html template
	htmltemp = __TEMP_DIR + "/plot_temp.html"
	# open result html to write
	outputbarfilename = __TEMP_DIR + "/auto_visual_bar_" + string.replace(fname,".xls", "") + ".html"
	outputbarfile = open(outputbarfilename, 'w')
	outputbarfile.truncate()

	outputscatterfilename = __TEMP_DIR + "/auto_visual_scatter_" + string.replace(fname,".xls", "") + ".html"
	outputscatterfile = open(outputscatterfilename, 'w')
	outputscatterfile.truncate()

	scriptinc = "<script src='filepath'></script>"


	with open(htmltemp) as htmlfile:
		for line in htmlfile:
			outputbarfile.write(line)
			outputscatterfile.write(line)

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
					# generate d3.js files
					if x_is_number and y_is_number :
						output = jsdirectory + "/scatterplot_x" + str(col1) + "_y" + str(col2) + ".js"
						generatePlot("scatter", rawxlsfile, output, x_index_name, y_index_name, col1, col2, datadirectory)
						inc = string.replace(scriptinc, "filepath", output)
						outputscatterfile.write(inc)
					elif x_is_number and y_is_string:
						output = jsdirectory + "/barplot_x" + str(col2) + "_y" + str(col1) + ".js"
						generatePlot("bar", rawxlsfile, output, y_index_name, x_index_name, col2, col1, datadirectory)
						inc = string.replace(scriptinc, "filepath", output)
						outputbarfile.write(inc)
					elif x_is_string and y_is_number:
						output = jsdirectory + "/barplot_x" + str(col1) + "_y" + str(col2) + ".js"
						generatePlot("bar", rawxlsfile, output, x_index_name, y_index_name, col1, col2, datadirectory)
						inc = string.replace(scriptinc, "filepath", output)
						outputbarfile.write(inc)
					else:
						print "ignoring the output"
						
	outdirpagename = __TEMP_DIR + "/auto_visual_dir_" + string.replace(fname,".xls", "") + ".html"
	outdirpage = open(outdirpagename, 'w')
	outdirpage.truncate()

	visuallist = []
	visuallist.append(string.replace(outputbarfilename, __TEMP_DIR, ""))
	visuallist.append(string.replace(outputscatterfilename, __TEMP_DIR, ""))

	return visuallist