from mmap import mmap, ACCESS_READ
from xlrd import open_workbook

print open_workbook('issue20.xls')

with open('issue20.xls', 'rb') as f:
	print open_workbook(
		file_contents=mmap(f.fileno(), 0, access = ACCESS_READ)
		)

aString = open('issue20.xls', 'rb').read()
print open_workbook(file_contents=aString)