'''
Created on Apr 11, 2015

@author: chenzhe
'''
def most_common(lst):
    return max(set(lst), key=lst.count)
    
class SheetUtil:
    
    def __init__(self, sheet):
        self.sheet = sheet
        self.headerrow_default = 0
        
        self.col2header = {}
        self.col2valuearr = {}
        self.col2valuetype = {}
        
        self.__get_header__()
        self.__get_valuearr__()
        
    def get_valuearr_twocols(self, col1, col2):
        valarr1, valarr2 = [], []
        for crow in range(self.sheet.rown):
            if crow == self.headerrow_default:
                continue
            value1 = None
            value2 = None
            if self.sheet.corr2value.has_key((crow, col1)):
                value1 = self.sheet.corr2value[(crow, col1)]
            if self.sheet.corr2value.has_key((crow, col2)):
                value2 = self.sheet.corr2value[(crow, col2)]
            valarr1.append(value1)
            valarr2.append(value2)
        return valarr1, valarr2
            
        
    def get_header(self, ccol):
        if self.col2header.has_key(ccol):
            return self.col2header[ccol]
        return None
        
    def get_valuearr(self, ccol):
        if self.col2valuearr.has_key(ccol):
            return self.col2valuearr[ccol]
        return []

    def get_valuetype(self, ccol):
        if self.col2valuetype.has_key(ccol):
            return self.col2valuetype[ccol]
        return None
        
    def __get_header__(self):
        for ccol in range(self.sheet.coln):
            cheader = None
            if self.sheet.corr2value.has_key(self.headerrow_default):
                cheader = self.sheet.corr2value[(self.headerrow_default, ccol)]
            self.col2header[ccol] = cheader
                
    def __get_valuearr__(self):
        for ccol in range(self.sheet.coln):
            valuearr, typearr = [], []
            for crow in range(self.sheet.rown):
                if crow == self.headerrow_default:
                    continue
                cval = None
                if self.sheet.corr2value.has_key((crow, ccol)):
                    cval = self.sheet.corr2value[(crow, ccol)]
                ctype = cval
                valuearr.append(cval)
                typearr.append(ctype)
                
            self.col2valuearr[ccol] = valuearr
            self.col2valuetype[ccol] = most_common(typearr)
                