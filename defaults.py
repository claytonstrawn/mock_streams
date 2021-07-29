import numpy as np
from unyt import mh

def lookup(var,dictionary):
    if var in dictionary.keys():
        return dictionary[var]
    else:
        return eval(var)    
    

Rvir = 100 #kpc
Mvir = 1e12 #Msun
a = 0.5 #expansion_parameter
z = 1.0 #redshift
n = 200 #cells across in each direction
box_size = 'Rvir' #kpc, diameter in each dimension
startpoint = [0,0,0] #center of simulation
stream_rotation = 0.0 #by default, streams non-rotating
n_streams = 3 #by default, 3 streams
stream_size_growth = 1 #by default, streams grow linearly (i.e. cones)
stream_width = {1:[40],2:[15,30],3:[10,15,30],4:[5,10,15,30]} #default stream size distribution
endpoint = 'random' #the endpoint of the streams will be anywhere in the plane
dist_method = 'radial' #options are "radial", "slab", and "min"
interface_thickness = 3  #kpc
density_contrast = 'separate' #if specified, ignore stream_density and stream_temperature
stream_temperature = 1e4 #K
bulk_temperature = 1e6 #K
stream_density = 10**-2 #cm-3
bulk_density = 10**-4 #cm-3
stream_metallicity = 10**-0.05 #Zsun
interface_metallicity = 10**0.03 #Zsun
bulk_metallicity = 10**0.23 #Zsun
beta = 1.47 #from simulations

s = 1.0
eta = 1.0
fh = 1.0
ths = 1.0
thh = 1.0