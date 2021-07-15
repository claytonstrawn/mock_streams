import numpy as np

def lookup(var,dictionary):
    if var in dictionary.keys():
        return dictionary[var]
    else:
        return eval(var)

#default setup arguments

Rvir = 100 #kpc
Mvir = 1e12 #Msun
a = 1.0 #expansion_parameter
z = 0.0 #redshift
n = 200 #cells across in each direction
box_size = 200 #kpc, diameter in each dimension

#geometry default arguments

startpoint = [0,0,0]

stream_rotation = 0
n_streams = 3
stream_size_growth = 1
stream_width = {1:[40],2:[15,30],3:[10,15,30],4:[5,10,15,30]}
endpoint = 'random'
dist_method = 'radial'
interface_thickness = 3

#math default arguments
density_contrast = 'separate'
pressure_eq = True

stream_temperature = 1e4
bulk_temperature = 1e6

stream_density = 10**-2
bulk_density = 10**-4

stream_metallicity = 10**-0.05
interface_metallicity = 10**0.03
bulk_metallicity = 10**0.23

beta = -1.47

