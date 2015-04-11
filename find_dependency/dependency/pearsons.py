'''
Created on Apr 10, 2015

@author: chenzhe
'''

import numpy as np

from scipy.stats.stats import pearsonr

class PearsonsCorrelation:
    
    def calc(self, valarr1, valarr2):
        var1 = np.var(valarr1)
        var2 = np.var(valarr2)
        if var1 == 0 or var2 == 0:
            return 1
        (pearson, conf) = pearsonr(valarr1, valarr2)
        return pearson
    
    
if __name__ == '__main__':
    valarr1 = [1, 1, 2]
    valarr2 = [2, 2, 4]
    pearson = PearsonsCorrelation()
    print pearson.calc(valarr1, valarr2)
    
    