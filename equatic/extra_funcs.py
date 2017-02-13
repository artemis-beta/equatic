import math

def add_quad(list_):
    out = list_[0]**2
    for val in list_:
        out+=val**2
    return math.pow(out, 0.5)