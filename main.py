import numpy as np
import yt
import trident
import mock_streams.defaults
import mock_streams.distance_checks

def main_function(geo_args, phys_args):
    background_grid,Rvir = do_setup()
    phase_grid = identify_phases(background_grid, geo_args,Rvir)
    fields = create_fields(background_grid, phase_grid, phys_args, Rvir)
    ds = convert_to_dataset(background_grid, fields)
    return ds

def do_setup(Rvir=100,n=50,box_size = 200):
    max_size = box_size/2
    x_vals = np.linspace(-max_size,max_size,n)
    y_vals = np.linspace(-max_size,max_size,n)
    z_vals = np.linspace(-max_size,max_size,n)

    xs = np.tile(x_vals,(n,n,1)).transpose((2,1,0))
    ys = np.tile(y_vals,(n,n,1)).transpose((0,1,2))
    zs = np.tile(z_vals,(n,n,1)).transpose((1,2,0))
    
    if not Rvir:
        Rvir = box_size/2
    return (xs,ys,zs),Rvir

#geometry section 
#code leader: Parsa

#random given values for 2-3D points along the sightline

#defines the x,y,and z coordinates

def identify_phases(background_grid, geo_args,Rvir):
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]
    
    phase_types = mock_streams.distance_checks.variable_distance_check(xs,ys,zs,Rvir)
    return phase_types

#math section 
#code leader: Jewon

def temperature_field(background_grid, phase_types):
    temperature = background_grid[0] * 0.0
    temperature[phase_types == 1] = mock_streams.defaults.temperature_1
    temperature[phase_types == 2] = mock_streams.defaults.temperature_2
    temperature[phase_types == 3] = mock_streams.defaults.temperature_3
    return temperature

def density_field(background_grid, phase_types, Rvir):
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]

    rho_0 = xs * 0.0
    rs = np.sqrt(xs**2+ys**2+zs**2)
    beta = mock_streams.defaults.beta

    rho_0[phase_types == 1] = mock_streams.defaults.rho_0_1
    rho_0[phase_types == 2] = mock_streams.defaults.rho_0_2
    rho_0[phase_types == 3] = mock_streams.defaults.rho_0_1
    
    density = rho_0 * (rs/Rvir)**beta
    return density

def metallicity_field(background_grid, phase_types):
    metallicity = background_grid[0] * 0.0
    metallicity[phase_types == 1] = mock_streams.defaults.metallicity_1
    metallicity[phase_types == 2] = mock_streams.defaults.metallicity_2
    metallicity[phase_types == 3] = mock_streams.defaults.metallicity_3
    return metallicity

def create_fields(background_grid, phase_types, phys_args, Rvir):
    fields = []
    fields.append(density_field(background_grid, phase_types, Rvir))
    fields.append(temperature_field(background_grid, phase_types))
    fields.append(metallicity_field(background_grid, phase_types))
    return fields

#yt section 
#code leader: Vayun
def convert_to_dataset(background_grid, fields): #assuming that the 'fields' parameter has fields ordered with the following: densities, temperatures, metallicities.
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]

    data = {('gas','density'):(fields[0], 'g*cm**(-3)'),('gas','temperature'):(fields[1],'K'),('gas','metallicity'):(fields[2],'Zsun')}
    bbox = np.array([[np.amin(xs),np.amax(xs)],[np.amin(ys),np.amax(ys),],[np.amin(zs),np.amax(zs),]])
    ds = yt.load_uniform_grid(data, fields[0].shape, length_unit="kpc", bbox=bbox)
    return ds

def create_ion_fields(ds): #for analysis of created dataset
    trident.add_ion_fields(ds, ions=['O VI'], ftype="gas")
    yt.ProjectionPlot(ds, 0, "O_p5_ion_fraction")
    yt.ProjectionPlot(ds, 0, "O_p5_number_density")
    yt.ProjectionPlot(ds, 0, "O_p5_density")
    yt.ProjectionPlot(ds, 0, "O_p5_mass")
