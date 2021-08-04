import numpy as np
import unyt

def temperature_field(background_grid, phase_types, model):
    Rvir = model['Rvir']
    
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]

    temp_0 = xs * 0.0
    temperature = xs * 0.0
    beta = xs * 0.0
    rs = np.sqrt(xs**2+ys**2+zs**2)

    B1 = model['stream_temperature_beta']
    B3 = model['bulk_temperature_beta']
    if B1<0 or B3<0:
        print('warning! beta is intended to be positive (higher densities in center)')
    B2 = (B1 + B3) / 2

    T1 = model['stream_temperature']
    T3 = model['bulk_temperature']
    T2 = np.sqrt(T1*T3)

    temp_0[phase_types == 1] = T1
    temp_0[phase_types == 2] = T2
    temp_0[phase_types == 3] = T3

    beta[phase_types == 1] = B1
    beta[phase_types == 2] = B2
    beta[phase_types == 3] = B3

    temperature[(rs/Rvir) > 0.1] = temp_0[rs/Rvir > 0.1] * (rs[rs/Rvir > 0.1]/Rvir)**-beta[rs/Rvir > 0.1]
    temperature[(rs/Rvir) <= 0.1] = temp_0[rs/Rvir <= 0.1] * 0.1**-beta[rs/Rvir <= 0.1]

    return temperature

def density_field(background_grid, phase_types, model):
    Rvir = model['Rvir']
    
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]

    rho_0 = xs * 0.0
    density = xs * 0.0
    beta = xs * 0.0
    rs = np.sqrt(xs**2+ys**2+zs**2)

    B1 = model['stream_density_beta']
    B3 = model['bulk_density_beta']
    if B1<0 or B3<0:
        print('warning! beta is intended to be positive (higher densities in center)')
    B2 = (B1 + B3) / 2
    
    R1 = model['stream_density']
    R3 = model['bulk_density']
    R2 = np.sqrt(R1*R3)
    
    rho_0[phase_types == 1] = R1
    rho_0[phase_types == 2] = R2
    rho_0[phase_types == 3] = R3

    beta[phase_types == 1] = B1
    beta[phase_types == 2] = B2
    beta[phase_types == 3] = B3
    
    density[(rs/Rvir) > 0.1] = rho_0[rs/Rvir > 0.1] * (rs[rs/Rvir > 0.1]/Rvir)**-beta[rs/Rvir > 0.1]
    density[(rs/Rvir) <= 0.1] = rho_0[rs/Rvir <= 0.1] * 0.1**-beta[rs/Rvir <= 0.1]
    return density

def metallicity_field(background_grid, phase_types, model):
    Rvir = model['Rvir']
    
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]

    met_0 = xs * 0.0
    metallicity = xs * 0.0
    beta = xs * 0.0
    rs = np.sqrt(xs**2+ys**2+zs**2)

    B1 = model['stream_metallicity_beta']
    B2 = model['interface_metallicity_beta']
    B3 = model['bulk_metallicity_beta']
    if B1<0 or B2 < 0 or B3<0:
        print('warning! beta is intended to be positive (higher densities in center)')

    M1 = model['stream_metallicity']
    M2 = model['interface_metallicity']
    M3 = model['bulk_metallicity']

    met_0[phase_types == 1] = model['stream_metallicity']
    met_0[phase_types == 2] = model['interface_metallicity']
    met_0[phase_types == 3] = model['bulk_metallicity']

    beta[phase_types == 1] = B1
    beta[phase_types == 2] = B2
    beta[phase_types == 3] = B3

    metallicity[(rs/Rvir) > 0.1] = met_0[rs/Rvir > 0.1] * (rs[rs/Rvir > 0.1]/Rvir)**-beta[rs/Rvir > 0.1]
    metallicity[(rs/Rvir) <= 0.1] = met_0[rs/Rvir <= 0.1] * 0.1**-beta[rs/Rvir <= 0.1]
    return metallicity

def velocity_field(background_grid, phase_types,model):
    Rvir = model['Rvir']
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]

    velocity_x = xs*0.0
    velocity_y = xs*0.0
    velocity_z = xs*0.0

    velocity_x = x_velocity(xs, ys, zs, Rvir).transpose((0,2,1))
    velocity_y = y_velocity(xs, ys, zs, Rvir).transpose((0,2,1))
    velocity_z = z_velocity(xs, ys, zs, Rvir).transpose((0,2,1))

    velocity_x[phase_types > 1] = 0
    velocity_y[phase_types > 1] = 0
    velocity_z[phase_types > 1] = 0

    return velocity_x, velocity_y, velocity_z

def get_v(Rvir):
    G = unyt.G
    M = unyt.Msun*1e12
    Rvir = unyt.kpc*Rvir

    v = np.sqrt(G*M/Rvir)
    v.convert_to_cgs()
    return v*unyt.s/unyt.cm

def dist_to_origin(x, y, z):
    return np.sqrt(x*x + y*y + z*z)

def x_velocity(x, y, z, Rvir):
    v = get_v(Rvir)
    tot = dist_to_origin(x, y, z)
    xvel = -(v/tot) * x
    return xvel

def y_velocity(x, y, z, Rvir):
    v = get_v(Rvir)
    tot = dist_to_origin(x, y, z)
    yvel = -(v/tot) * y
    return yvel

def z_velocity(x, y, z, Rvir):
    v = get_v(Rvir)
    tot = dist_to_origin(x, y, z)
    zvel = -(v/tot) * z
    return zvel