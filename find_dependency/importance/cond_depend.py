'''
Created on Apr 10, 2015

@author: chenzhe
'''

class ConditionalDependence:

    def calc(self, pairarr):
        if len(pairarr) == 0:
            return 0
        
        lval2rvalarr = {}
        rval2lvalarr = {}
        for (lval, rval) in pairarr:
            if not lval2rvalarr.has_key(lval):
                lval2rvalarr[lval] = set([])
            lval2rvalarr[lval].add(rval)
            if not rval2lvalarr.has_key(rval):
                rval2lvalarr[rval] = set([])
            rval2lvalarr[rval].add(lval)
            
        lcond = float(len(lval2rvalarr))/len(pairarr)
        rcond = float(len(rval2lvalarr))/len(pairarr)
        
        print lcond, rcond
        
if __name__ == '__main__':
    pairarr = [('a', 'c'), ('a', 'c'), ('a', 'b'), ('d', 'e')]
    cond = ConditionalDependence()
    cond.calc(pairarr)