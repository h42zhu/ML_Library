# library for stats functions
import math

# return the Probablity of an obs that follows Chi Square distr
def inverse_chi2(chi, df):
    m = chi/ 2.0
    s = term = math.exp(-m)
    for i in range(1, df // 2):
        term *= m / i
        s += term
    return min(s, 1.0)