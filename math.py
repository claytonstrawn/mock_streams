import numpy as np
from mock_streams.defaults import lookup

def temperature_field(background_grid, phase_types, phys_args):
    T3 = lookup('bulk_temperature',phys_args)
    density_contrast = lookup('density_contrast',phys_args)
    if density_contrast == 'separate':
        T1 = lookup('stream_temperature',phys_args)
    else:
        T1 = T3/density_contrast
    T2 = np.sqrt(T1*T3)

    temperature = background_grid[0] * 0.0
    temperature[phase_types == 1] = T1
    temperature[phase_types == 2] = T2
    temperature[phase_types == 3] = T3
    return temperature

def density_field(background_grid, phase_types, phys_args, Rvir):
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]

    rho_0 = xs * 0.0
    density = xs * 0.0
    rs = np.sqrt(xs**2+ys**2+zs**2)
    beta = lookup('beta',phys_args)
    if beta>0:
        print('warning! beta is intended to be negative (higher densities in center)')
    
    R3 = lookup('bulk_density',phys_args)
    density_contrast = lookup('density_contrast',phys_args)
    if density_contrast == 'separate':
        R1 = lookup('stream_density',phys_args)
    else:
        R1 = R3*density_contrast
    R2 = np.sqrt(R1*R3)    
    
    rho_0[phase_types == 1] = R1
    rho_0[phase_types == 2] = R2
    rho_0[phase_types == 3] = R3
    
    density[(rs/Rvir) > 0.1] = rho_0[rs/Rvir > 0.1] * (rs[rs/Rvir > 0.1]/Rvir)**beta
    density[(rs/Rvir) <= 0.1] = rho_0[rs/Rvir <= 0.1] * 0.1**beta
    return density

def metallicity_field(background_grid, phase_types, phys_args):
    metallicity = background_grid[0] * 0.0
    metallicity[phase_types == 1] = lookup('stream_metallicity',phys_args)
    metallicity[phase_types == 2] = lookup('interface_metallicity',phys_args)
    metallicity[phase_types == 3] = lookup('bulk_metallicity',phys_args)
    return metallicity
