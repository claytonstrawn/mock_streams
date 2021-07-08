import numpy as np
import yt
import trident
from mock_streams import geometry
from mock_streams import math
from mock_streams import defaults
#from mock_streams import yt_interface

def main_function(geo_args, phys_args):
    background_grid,Rvir = do_setup()
    phase_grid = identify_phases(background_grid, geo_args,Rvir)
    fields = create_fields(background_grid, phase_grid, phys_args, Rvir)
    filename = convert_to_dataset(background_grid, fields)
    ds = load_dataset(filename)
    return ds

def do_setup(Rvir=100,n=200,box_size = 200):
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
def identify_phases(background_grid, geo_args,Rvir):
    #geo_args options:
    #stream_rotation = 0 -> no rotation
    #stream_rotation = 1 -> 1 full rotation
    #n_streams = 1 -> only one stream
    #n_streams = 3 -> 3 discrete streams
    #stream_size_growth = 0 -> Rs constant with distance to center
    #stream_size_growth = 1 -> Rs proportional to (r/Rvir)**1
    #stream_size_growth = 2.1 -> Rs proportional to (r/Rvir)**2.1
    #stream_width = 50 -> Rs = 50 at Rvir
    #endpoint = 'random' -> randomize the endpoints
    #endpoint = 'fixed' -> use the fixed default endpoints
    #endpoint = [100,0,0] -> go to the point [100,0,0]

    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]
    
    phase_types = geometry.variable_distance_check(xs,ys,zs,Rvir)
    return phase_types

#math section 
#code leader: Jewon
def create_fields(background_grid, phase_types, phys_args, Rvir):
    #phys_args options:
    #density_contrast = 1 -> no difference b/w stream and bulk, rho_s/rho_b = 1
    #density_contrast = 10 -> rho_s/rho_b = 10
    #beta = -1.5 -> all three components follow same powerlaw of rho_0 * (r/Rvir)**-1.5
    #beta = (-1.5,-2.5) -> stream,bulk follow different powerlaws of rho_0 * (r/Rvir)**-1.5 and -2.5, respectively
    #metallicity_growth = 0 -> stream, bulk, interface all constant metallicity from defaults
    #metallicity_growth = -1 -> stream metallicity increases closer to center at Z_0 *(r/Rvir)**-1
    #temperatures = 'constant' -> keep temperature constant inside the structure
    
    fields = {}
    fields['density']=math.density_field(background_grid, phase_types, Rvir)
    fields['temperature']=math.temperature_field(background_grid, phase_types)
    fields['metallicity']=math.metallicity_field(background_grid, phase_types)
    return fields

#yt section 
#code leader: Vayun
def convert_to_dataset(background_grid, fields, filename='mock.h5'): #assuming that the 'fields' parameter has fields ordered with the following: densities, temperatures, metallicities.
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]
    
    #will probably make a dictionary
    
    data = {('gas','density'):(fields[0], 'g*cm**(-3)'),('gas','temperature'):(fields[1],'K'),('gas','metallicity'):(fields[2],'Zsun')}
    bbox = np.array([[np.amin(xs),np.amax(xs)],[np.amin(ys),np.amax(ys),],[np.amin(zs),np.amax(zs),]])
    ds = yt.load_uniform_grid(data, fields[0].shape, length_unit="kpc", bbox=bbox)
    
    density_with_units = yt.YTArray(fields[0], 'g*cm**(-3)')
    temperature_with_units = yt.YTArray(fields[1], 'K')
    metallicity_with_units = yt.YTArray(fields[2], 'Zsun')
    
    my_data = {('data','density'): (density_with_units), ('data','temperature'): (temperature_with_units), ('data','metallicity'): (metallicity_with_units)}
    temp_ds = {}
    yt.save_as_dataset(temp_ds, filename, my_data)
    return filename
   
def load_dataset(filename):
    temp_ds = yt.load(filename)

    def density(field, data):
        return (data['data','density'])

    def temperature(field, data):
        return (data['data','temperature'])

    def metallicity(field, data):
        return (data['data','density'])

    temp_ds.add_field(("gas", "density"), function=density, sampling_type="local", units='g/cm**3')
    temp_ds.add_field(("gas", "density"), function=temperature, sampling_type="local", units='K')
    temp_ds.add_field(("gas", "density"), function=metallicity, sampling_type="local", units='Zsun')


    data = {('gas','density'):(temp_ds.data['gas','density'])}
    bbox = np.array([[-100,100], [-100,100], [-100,100]])
    ds = yt.load_uniform_grid(data, temp_ds.data['gas','density'].shape, length_unit="kpc", bbox=bbox)
    return ds
    

def create_ion_fields(ds): #for analysis of created dataset
    trident.add_ion_fields(ds, ions=['O VI'], ftype="gas")
    yt.ProjectionPlot(ds, 0, "O_p5_ion_fraction")
    yt.ProjectionPlot(ds, 0, "O_p5_number_density")
    yt.ProjectionPlot(ds, 0, "O_p5_density")
    yt.ProjectionPlot(ds, 0, "O_p5_mass")
