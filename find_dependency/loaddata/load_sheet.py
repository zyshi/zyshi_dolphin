'''
Created on Apr 10, 2015

@author: chenzhe
'''

import copy

class Sheet:
    def __init__(self):
        self.sheetname = ''
        self.rown = 0
        self.coln = 0
        
        self.corr2type = {}
        self.corr2value = {}
        
        self.type2corrarr = {}
    
    def is_empty(self):
        if self.rown == 0 or self.coln == 0:
            return True
        return False

    def add_cell(self, crow, ccol, ctype, cval, sheetname):
        if len(self.sheetname) != 0 and self.sheetname != sheetname:
            print 'ERROR'
        
        self.sheetname = sheetname
        if crow > self.rown:
            self.rown = crow
        if ccol > self.coln:
            self.coln = ccol
            
        self.corr2type[(crow, ccol)] = ctype
        self.corr2value[(crow, ccol)] = cval
        
        if not self.type2corrarr.has_key(ctype):
            self.type2corrarr[ctype] = []
        self.type2corrarr[ctype].append((crow, ccol))
        
    def __str__(self):
        cstr = ''
        for (crow, ccol), cval in self.corr2value.items():
            cstr += str(crow) + ','+str(ccol) + '\t'+str(cval) + '\n'
        return cstr
    
class LoadSheet:
    def __init__(self):
        pass
    
    def load_sheets(self, filepath):
        sheetarr = []
        
        fin = open(filepath)
        presheet = Sheet()
        for line in fin:
            strarr = line.strip().split('||')
            if len(strarr) != 5:
                continue
            sheetname = strarr[0].strip()
            crow = int(strarr[1].strip())
            ccol = int(strarr[2].strip())
            ctype = int(strarr[3].strip())
            cval = strarr[4].strip()
            
            if (not presheet.is_empty()) and sheetname != presheet.sheetname:
                sheetarr.append(copy.deepcopy(presheet))
                presheet = Sheet()
            
            presheet.add_cell(crow, ccol, ctype, cval, sheetname)
                
        if not presheet.is_empty():
            sheetarr.append(presheet)
        return sheetarr
            
if __name__ == '__main__':
    load = LoadSheet()
    filepath = '/home/chenzhe/test.txt'
    sheetarr = load.load_sheets(filepath)
    for csheet in sheetarr:
        print csheet
    
    
    
                

    
                