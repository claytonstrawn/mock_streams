import numpy as np

def lookup(var,dictionary):
    if var in dictionary.keys():
        return dictionary[var]
    else:
        return eval(var)

#default setup arguments

Rvir = 100 #kpc
Mvir = 1e12 #Msun
n = 200 #cells across in each direction
box_size = 200 #kpc, diameter in each dimension

#geometry default arguments

x1 = 0
y1 = 0
z1 = 0

stream_rotation = 0
n_streams = 1
stream_size_growth = 1
stream_width = 50
endpoint = 'random'
dist_method = 'radial'
interface_thickness = 5

#math default arguments
temperature_1 = 1e4
temperature_3 = 1e6
def temperature_2_function(T1,T3):
    return np.sqrt(T1*T3)
temperature_2 = temperature_2_function(temperature_1,temperature_3)

rho_0_1 = 10**-3.5
rho_0_3 = 10**-5.4
def rho_0_2_function(R1,R3):
    return np.sqrt(R1*R3)
rho_0_2 = rho_0_2_function(rho_0_1,rho_0_3)

metallicity_1 = 10**-0.05
metallicity_2 = 10**0.03
metallicity_3 = 10**0.23

beta = -1.47

