from mock_streams import defaults
import numpy as np
import unyt

def temperature_field(background_grid, phase_types):
    temperature = background_grid[0] * 0.0
    temperature[phase_types == 1] = defaults.temperature_1
    temperature[phase_types == 2] = defaults.temperature_2
    temperature[phase_types == 3] = defaults.temperature_3
    return temperature

def density_field(background_grid, phase_types, phys_args, Rvir):
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]

    rho_0 = xs * 0.0
    density = xs * 0.0
    rs = np.sqrt(xs**2+ys**2+zs**2)
    beta = defaults.beta

    rho_0[phase_types == 1] = defaults.rho_0_1
    rho_0[phase_types == 2] = defaults.rho_0_2
    rho_0[phase_types == 3] = defaults.rho_0_3
    
    density[rs/Rvir > 0.1] = rho_0[rs/Rvir > 0.1] * (rs[rs/Rvir > 0.1]/Rvir)**beta
    density[rs/Rvir <= 0.1] = rho_0[rs/Rvir <= 0.1] * 0.1**beta
    return density

def metallicity_field(background_grid, phase_types):
    metallicity = background_grid[0] * 0.0
    metallicity[phase_types == 1] = defaults.metallicity_1
    metallicity[phase_types == 2] = defaults.metallicity_2
    metallicity[phase_types == 3] = defaults.metallicity_3
    return metallicity

def velocity_field(background_grid, phase_types, Rvir):
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]

    velocity = x_velocity(xs, ys, zs, Rvir), y_velocity(xs, ys, zs, Rvir), z_velocity(xs, ys, zs, Rvir)
    return velocity

def get_v(Rvir):
    G = unyt.G
    M = unyt.Msun*1e12
    Rvir = unyt.kpc*Rvir

    v = np.sqrt(G*M/Rvir)
    v.convert_to_cgs()
    return v

def dist_to_origin(x, y, z):
    return np.sqrt(x*x + y*y + z*z)

def x_velocity(x, y, z, Rvir):
    v = get_v(Rvir)
    tot = dist_to_origin(x, y, z)
    xvel = (v/tot) * x - x
    return xvel

def y_velocity(x, y, z, Rvir):
    v = get_v(Rvir)
    tot = dist_to_origin(x, y, z)
    yvel = (v/tot) * y - y
    return yvel

def z_velocity(x, y, z, Rvir):
    v = get_v(Rvir)
    tot = dist_to_origin(x, y, z)
    zvel = (v/tot) * z - z
    return zvel




