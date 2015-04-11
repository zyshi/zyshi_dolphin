'''
Created on Apr 10, 2015

@author: chenzhe
'''

class ConditionalDependence:

    def calc(self, valarr1, valarr2):
        if len(valarr1) == 0:
            return 0
        if len(valarr2) == 0:
            return 0
        if len(valarr1) != len(valarr2):
            print 'ERROR'
            return 0
        
        clength = len(valarr1)
        
        lval2rvalarr = {}
        rval2lvalarr = {}
        for i in range(clength):
            lval = valarr1[i] 
            rval = valarr2[i]
            if not lval2rvalarr.has_key(lval):
                lval2rvalarr[lval] = set([])
            lval2rvalarr[lval].add(rval)
            if not rval2lvalarr.has_key(rval):
                rval2lvalarr[rval] = set([])
            rval2lvalarr[rval].add(lval)
            
        lcond = float(len(lval2rvalarr))/clength
        rcond = float(len(rval2lvalarr))/clength
        
        return max(lcond, rcond)
#         print lcond, rcond
        
if __name__ == '__main__':
    pairarr = [('a', 'c'), ('a', 'c'), ('a', 'b'), ('d', 'e')]
    cond = ConditionalDependence()
    cond.calc(pairarr)