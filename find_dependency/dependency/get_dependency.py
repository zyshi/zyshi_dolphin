'''
Created on Apr 11, 2015

@author: chenzhe
'''
from loaddata.load_sheet import LoadSheet
from loaddata.sheet_util import SheetUtil
from importance.entropy import SheetEntropy
from dependency.cond_depend import ConditionalDependence
from dependency.pearsons import PearsonsCorrelation


class GetDependency:
    
    def __init__(self, csheet):
        self.sheetutil = SheetUtil(csheet)
        self.getentropy = SheetEntropy()
        self.conddependence = ConditionalDependence()
        self.pearsons = PearsonsCorrelation()
         
#       0:numerics; 1:string; 2:formula
    def getScoreCoverage(self):
        coor2score = {}
        for col1 in range(csheet.coln):
            for col2 in range(col1):
                
                if col1 == 0 or col2 == 0:
                    print
#                 type1 = self.sheetutil.get_valuetype(col1)
#                 type2 = self.sheetutil.get_valuetype(col2)
                valarr1, valarr2 = self.sheetutil.get_valuearr_twocols(col1, col2)
                cscore = self.conddependence.calc(valarr1, valarr2)
                coor2score[(col1, col2)] = cscore
        
        sortdict = sorted(coor2score.iteritems(), key=lambda x:x[1], reverse = True)
        for (col1, col2), score in sortdict:
            print col1, col2, score
        
    def getScoreImportance(self, ccol):
        valarr = self.sheetutil.get_valuearr(ccol)
        return self.getentropy.calc(valarr)
    
    def selectByImportance(self):
        col2score = {}
        for ccol in range(csheet.coln):
            cscore = self.getScoreImportance(ccol)
            col2score[ccol] = cscore
#             print ccol, cscore
            
        sortdict = sorted(col2score.iteritems(), key=lambda x:x[1], reverse = True)
        for ccol, cscore in sortdict:
            print ccol, cscore
    
    
if __name__ == '__main__':
    filepath = '/home/chenzhe/test/test.txt'
    loadsheet = LoadSheet()
    sheetarr = loadsheet.load_sheets(filepath)
    for csheet in sheetarr:
        print csheet.sheetname
        getdependency = GetDependency(csheet)
#         getdependency.selectByImportance()
        getdependency.getScoreCoverage()
