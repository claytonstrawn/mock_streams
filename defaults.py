import numpy as np
from unyt import mh

def lookup(var,dictionary=None):
    if dictionary is None or var not in dictionary.keys():
        return eval(var)    
    else:
        return dictionary[var]
    

Rvir = 100. #kpc
Mvir = 1e12 #Msun
a = 0.5 #expansion_parameter
z = 1.0 #redshift
n = 200 #cells across in each direction
box_size = 'Rvir' #kpc, diameter in each dimension
startpoint = [0.,0.,0.] #center of simulation
stream_rotation = 0.1 #by default, streams are rotating
n_streams = 3 #by default, 3 streams
stream_size_growth = 1 #by default, streams grow linearly (i.e. cones)
stream_width = {1:[40],2:[15,30],3:[10,15,30],4:[5,10,15,30]} #default stream size distribution
endpoint = 'random' #the endpoint of the streams will be anywhere in the plane
dist_method = 'slab' #options are "radial", "slab", and "min"
interface_thickness = 3.  #kpc
density_contrast = 'separate' #if specified, ignore stream_density and stream_temperature
stream_temperature = 10.**4.6 #K
bulk_temperature = 10.**6.6 #K
stream_density = 10.**-3.5 #cm-3
bulk_density = 10.**-5.4 #cm-3
stream_metallicity = 10.**-1.104 #Zsun
interface_metallicity = 10.**-0.869 #Zsun
bulk_metallicity = 10.**-0.233 #Zsun
stream_density_beta = 2.29 #from simulations
bulk_density_beta = 1.54
stream_temperature_beta = -0.80
bulk_temperature_beta = 0.54
stream_metallicity_beta = 1.17
interface_metallicity_beta = 1.10 #from simulations
bulk_metallicity_beta = 0.46
beta = 1.5

s = 1.0
eta = 1.0
fh = 1.0
ths = 1.0
thh = 1.0