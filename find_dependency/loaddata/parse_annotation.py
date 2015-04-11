'''
@author: Zhongyi SHi
@contact: zyshi@umich.edu
'''
import copy
import re
import load_sheet
import string
from collections import OrderedDict

class AnnotationTable:
    def __init__(self):
        # hash table of all possible annotations
        # key: (row, coln), value: string
        self.annotations = {}

    # populate an annotation table for incoming sheet
    def getAnnotationTable(self, sheet):
        # populate all possible annotations
        # Assume annotations are string
        for i in range(0, sheet.rown):
            for j in range (0, sheet.coln):
                if sheet.corr2type.has_key((i, j)) and sheet.corr2type[(i, j)] == 1:
                    self.annotations[(i, j)] = sheet.corr2value[(i, j)]

    # return a list of possible annotations for the given cell
    def getAnnotation(self, row, coln, annoArr, isTop):
        # populate all  possible top header 
        # top + row#
        ans = OrderedDict()
        if isTop:
            for i in range(0, row):
                if self.annotations.has_key((i, coln)):
                  topID = "top" + str(i) + "," + str(coln)
                  ans[topID] = self.annotations[(i, coln)]
        else:
        # TOD0: How to denote the cell not in this row in formular
        # find possible left header
            for i in range (0, coln):
                if self.annotations.has_key((row, i)):
                    leftID = "left" + str(i) + str(row)
                    ans[leftID] = self.annotations[(row, i)]
        annoArr.append(ans)
        return ans

def isRow(pendingRow):
    ans = re.findall(r'[A-Z]\d+', pendingRow)
    print ans

# convert excel coln# to index#
def col2num(col):
    if isinstance(col, int):
        return col
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num - 1


def parseCoor(coor, opCoorArr):
    row = re.search(r'\d+', coor).group()
    rown = int(row)
    coln = col2num(string.replace(coor, row, ""))
    opCoorArr.append((rown, coln))
    return (rown, coln)

def operandExtractor(formula):
    # TODO: SQRT?? ^2
    # print formula
    parts = re.split("([()+-/*])", formula.replace(" ", ""))
    operands = []
    for itr in parts:
        if itr == '':
            parts.remove(itr)
        else:
            m = re.match(r'[A-Z]*\d*', itr)
            if m.group(0) != '':
                operands.append(m.group(0))
    # print operands
    return operands

class FormulaBook:
    def __init__(self):
        self.formulaBook = {}

    def loadFormulas(self, sheet):
        for row in range(0, sheet.rown):
            for coln in range(0, sheet.coln):
                if sheet.corr2type.has_key((row, coln)) and sheet.corr2type[(row, coln)] == 2:
                    self.formulaBook[(row, coln)] = sheet.corr2value[(row, coln)]
        return self.formulaBook

    def printBook(self):
        for itr in self.formulaBook:
            print itr
            print self.formulaBook[itr]

    def equation2semantic(formula, operands, ):
        print 'a'

if __name__ == '__main__':

    load = load_sheet.LoadSheet()
    # filepath = '/z/chenzhe-data/spreadsheet/webexcel/webexcel_sample5000_txt/'
    # filename = 'http:____britishhorseracing.com__images__inside_horseracing__media__2006_Fixture_List_by_date.xls'
    filename = 'test.txt'
    # sheetarr = load.load_sheets(filepath+"/"+filename)
    sheetarr = load.load_sheets(filename)
    # datadirectory = "/home/zyshi"
    # outFile = datadirectory + "/" + filename  
    outFileName = string.replace(filename, "txt", "out")

    outFile = open(outFileName, 'w')
    outFile.truncate()


    atable = AnnotationTable()

    # isRow("I2333")
    # operandExtractor("a")

    for csheet in sheetarr:
        atable  = AnnotationTable()

        # populate annotations table
        atable.getAnnotationTable(csheet)

        # get all formula
        book = FormulaBook()
        formulas = book.loadFormulas(csheet)
        # book.printBook()

        # generate semnantic formular
        for itr in formulas:
            print ""
            rown = itr[0] + 1
            coln = itr[1]
            annoArr = []
            operands = operandExtractor(formulas[itr])
            # insert op_res = 
            operandArr = []
            restFormula = formulas[itr]
            # dictionay mapping operand => (row, coln)
            print "=== original formula ==="
            print "rest = " + restFormula

            outFile.write(restFormula+"\n")

            print "=== operands list ==="
            print operands

            # parse coordinate based on operands
            for op in operands:
                parseCoor(op, operandArr)
            operandArr.append((rown, coln))
            print "=== operands' coor ===="
            print operandArr

            #TODO:
            isTop =  operandArr[0][0] == operandArr[1][0]
            for opcoor in operandArr:
                atable.getAnnotation(opcoor[0], opcoor[1], annoArr, isTop)
            print "=== candidate annotations ==="
            print annoArr

            # print len(annoArr)
            # print annoArr[len(annoArr) - 1]
            #TODO: filter candidates
            finalAnno = []
            for itr in annoArr:
                els = list(itr.items())
                # print "aaa"
                # print els[-1][1]
                # for it in itr:
                    # print itr[it]
                finalAnno.append(els[-1][1])

            print "=== final annotations ==="
            print finalAnno

            semnantic = finalAnno[len(finalAnno) - 1] + " = "
            semnantic += restFormula
            semnantic = string.replace(semnantic, "+", " + ")
            i = 0
            for op in operands:
                semnantic = string.replace(semnantic, op, finalAnno[i])
                i += 1
            print semnantic
            semnantic += '\n'
            outFile.write(semnantic)
