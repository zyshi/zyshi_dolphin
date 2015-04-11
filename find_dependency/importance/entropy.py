'''
Created on Apr 10, 2015

@author: chenzhe
'''

import math

class SheetEntropy:
    
    def calc(self, valarr):
        if len(valarr) == 0:
            return 0
        
        val2count = {}
        for cval in valarr:
#             print cval
            if not val2count.has_key(cval):
                val2count[cval] = 0
            val2count[cval] += 1
        
        centropy = 0
        for ccount in val2count.values():
            cprob = float(ccount) / len(valarr)
            centropy -= cprob * math.log(cprob)
        return centropy
        
        
if __name__ == '__main__':
    entropy = SheetEntropy()
    testarr = [0, 0, 1, 1]
    print entropy.calc(testarr)
        