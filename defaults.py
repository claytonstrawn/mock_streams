import numpy as np

#geometry default arguments
x1 = 0
y1 = 0
z1 = 0
x2 = 0
y2 = 100
z2 = 0

stream_radius_at_Rvir = 50
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

