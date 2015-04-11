'''
@author: Zhongyi SHi
@contact: zyshi@umich.edu
'''
import re
import load_sheet
import string

class AnnotationBook:
    def __init__(self, sheet):
        # hash table of all possible annotations
        # key: (row, coln), value: string
        self.annotations = self.__getAnnotationTable__(sheet)

    # populate an annotation table for incoming sheet
    def __getAnnotationTable__(self, sheet):
        # populate all possible annotations
        # Assume annotations are string
        
        annotations = {}
        # 0:numerics; 1:string; 2:formula
        strcorrarr = sheet.type2corrarr[1]
        for (crow, ccol) in strcorrarr:
            annotations[(crow, ccol)] = sheet.corr2value[(crow, ccol)]

        return annotations

    # return a list of possible annotations for the given cell
    def getAnnotation(self, row, col):
        # populate all  possible top header 
        # top + row#
        annotationdict = {}

        for crow in range(0, row):
            if self.annotations.has_key((crow, col)):
                annotationdict[(crow, col)] = self.annotations[(crow, col)]
        # TOD0: How to denote the cell not in this row in formular
        # find possible left header
        for ccol in range (0, col):
            if self.annotations.has_key((row, ccol)):
                annotationdict[(row, ccol)] = self.annotations[(row, ccol)]

        return annotationdict



class FormulaBook:
    def __init__(self, sheet):
        self.formula = self.loadFormulas(sheet)

    def loadFormulas(self, sheet):
        formulas = {}
        # 0:numerics; 1:string; 2:formula
        strcorrarr = sheet.type2corrarr[2]
        for (crow, ccol) in strcorrarr:
            formulas[(crow, ccol)] = sheet.corr2value[(crow, ccol)]

        return formulas

    def printBook(self):
        for itr in self.formulaBook:
            print itr
            print self.formulaBook[itr]



class ParseFormula:
    def __init__(self, sheet):
        
        self.opCoorArr = []
        self.annotationbook = AnnotationBook(sheet)
        self.formulabook = FormulaBook(sheet)
        
    def __col2num__(self, col):
        if isinstance(col, int):
            return col
        num = 0
        for c in col:
            if c in string.ascii_letters:
                num = num * 26 + (ord(c.upper()) - ord('A')) + 1
        return num - 1
    
    def __coor2name__(self, crow, ccol):
        crow += 1
        
        rightalpha = chr(ccol % 26 + ord('A'))
        leftalpha = ''
        if ccol / 26  != 0:
            leftalpha = chr(ccol / 26 + ord('A') - 1)
        
        return  leftalpha + rightalpha + str(crow)
        
    def __name2coor__(self, coor):
        row = re.search(r'\d+', coor).group()
        rown = int(row)
        coln = self.__col2num__(string.replace(coor, row, ""))
#         self.opCoorArr.append((rown, coln))
        return (rown-1, coln)
    
    def isValidCell(self, coor):
        cpattern = '^[A-Z]+[0-9]+$'
        if re.match(cpattern, coor):
            return True
        return False
    

    def filter_annotations(self, coor2anno):
        
        annocoor2count = {}
        for coor, annodict in coor2anno.items():
            for (crow, ccol) in annodict.keys():
                if not annocoor2count.has_key((crow, ccol)):
                    annocoor2count[(crow, ccol)] = 0
                annocoor2count[(crow, ccol)]  += 1
        
        duplicatearr = set()
        for (crow, ccol), ccount in annocoor2count.items():
            if ccount == len(coor2anno):
                duplicatearr.add((crow, ccol))
        
        newcoor2anno = {}        
        for (crow, ccol), annodict in coor2anno.items():
            annoarr = []
            for (arow, acol), annotation in annodict.items():
                if (arow, acol) in duplicatearr:
                    continue
                annoarr.append(annotation)
            newcoor2anno[(crow, ccol)] = annoarr
        
        return newcoor2anno
    
    def getSemanticFormula(self, frow, fcol, formula, coor2anno):
        fcoor = self.__coor2name__(frow, fcol)
        formula = fcoor + '=' + formula
        print formula
        # for (crow, ccol), anno in coor2anno.items():
        #     coor = self.__coor2name__(crow, ccol)
        #     formula = string.replace(formula, coor, str(anno))
        name2anno = {}

        for (crow, ccol), anno in coor2anno.items():
            coor = self.__coor2name__(crow, ccol)
            name2anno[coor] = anno
        print name2anno
        #     pattern = '^|[^A-Z]'+coor+'[^0-9]|$'
        #     formula = re.sub(pattern, str(anno), formula)
        #     # formula = string.replace(formula, coor, str(anno))
        return formula

    def parse_sheet(self):
        results = []
        for (frow, fcol), formula in self.formulabook.formula.items():
            semanticformula = self.parse_cell(frow, fcol, formula)
            results.append(semanticformula)
        return results

    def parse_cell(self, frow, fcol, formula):
        # TODO: SQRT?? ^2
        # print formula
        
        
        
        regex = re.compile('[\s%s]' % re.escape(string.punctuation))
        strarr = re.split(regex, formula)
        
        coor2anno = {}
        for coor in strarr:
            if len(coor) == 0:
                continue
            if not self.isValidCell(coor):
                continue
            (crow, ccol) = self.__name2coor__(coor)
            annodict = self.annotationbook.getAnnotation(crow, ccol)
            coor2anno[(crow, ccol)] = annodict
        coor2anno[(frow, fcol)] = (self.annotationbook.getAnnotation(frow, fcol))
        
        coor2anno = self.filter_annotations(coor2anno)
        return self.getSemanticFormula(frow, fcol, formula, coor2anno)

#         annoformula = []
#         return annoformula
            
        
        

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


    for csheet in sheetarr:
        parseformula = ParseFormula(csheet)
        resarr =  parseformula.parse_sheet()
        for cres in resarr:
            print cres
