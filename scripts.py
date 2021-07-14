import numpy as np
import yt
import trident
import os
from datetime import datetime

def create_number_density_plots(ds, ions, dimension = 2):
    path = 'savedplots ' + datetime.now().strftime(' %m.%d.%Y %H:%M:%S')
    pathsave = path + '/'
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
        
    trident.add_ion_fields(ds, ions=ions, ftype="gas")
    
    roman_values = (('I',1), ('IV',4), ('V',5), ('IX',9),('X',10),('XL',40),('L',50),('XC',90),('C',100),
                    ('CD', 400), ('D', 500), ('CM', 900), ('M',1000))
 
    def roman_value(roman):
        total=0
        for symbol,value in reversed(roman_values):
            while roman.startswith(symbol):
                total += value
                roman = roman[len(symbol):]
        return total
    
    
    for ion in ions:
        yt.SlicePlot(ds, dimension, ion.split(' ')[0] + '_p' + str(roman_value(ion.split(' ')[1])-1) +
                     '_number_density').save(pathsave)
        yt.ProjectionPlot(ds, dimension, ion.split(' ')[0] + '_p' + str(roman_value(ion.split(' ')[1])-1) +
                     '_number_density').save(pathsave)
