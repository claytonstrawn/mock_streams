import numpy as np
import yt
from unyt import mh

def create_dataset(fields, filename): #assuming that the 'fields' parameter has fields ordered with the following: densities, temperatures, metallicities.
    density_with_units = yt.YTArray(fields['density'], 'g*cm**(-3)')
    temperature_with_units = yt.YTArray(fields['temperature'], 'K')
    metallicity_with_units = yt.YTArray(fields['metallicity'], 'Zsun')
    velx_with_units = yt.YTArray(fields['velocity_x'], 'cm/s')
    vely_with_units = yt.YTArray(fields['velocity_y'], 'cm/s')
    velz_with_units = yt.YTArray(fields['velocity_z'], 'cm/s')
    xs_with_units = yt.YTArray(fields['xs'], 'kpc')
    ys_with_units = yt.YTArray(fields['ys'], 'kpc')
    zs_with_units = yt.YTArray(fields['zs'], 'kpc')
    phase_types_with_units = yt.YTArray(fields['phase_types'],'')
    
    my_data = {('data','density'): (density_with_units), ('data','temperature'): (temperature_with_units), \
               ('data','metallicity'): (metallicity_with_units), ('data','velocity_x'): (velx_with_units), \
               ('data','velocity_y'): (vely_with_units), ('data','velocity_z'): (velz_with_units), \
               ('data','x'):xs_with_units,('data','y'):ys_with_units,('data','z'):zs_with_units, \
               ('data','phase_types'):phase_types_with_units}
    
    temp_ds = {}
    yt.save_as_dataset(temp_ds, filename, my_data)
    return filename
    
def load_ds(filename,redshift):
    print(filename)
    temp_ds = yt.load(filename)

    def density(field, data):
        return (data['data','density'])

    def temperature(field, data):
        return (data['data','temperature'])

    def metallicity(field, data):
        return (data['data','metallicity'])
    
    def velocity_x(field, data):
        return (data['data','velocity_x'])
    
    def velocity_y(field, data):
        return (data['data','velocity_y'])
    
    def velocity_z(field, data):
        return (data['data','velocity_z'])
    
    def phase_types(field,data):
        return data['data','phase_types']

    temp_ds.add_field(("gas", "density"), function=density, sampling_type="local", units='g/cm**3')
    temp_ds.add_field(("gas", "temperature"), function=temperature, sampling_type="local", units='K')
    temp_ds.add_field(("gas", "metallicity"), function=metallicity, sampling_type="local", units='Zsun')
    temp_ds.add_field(("gas", "velocity_x"), function=velocity_x, sampling_type="local", units='cm/s')
    temp_ds.add_field(("gas", "velocity_y"), function=velocity_y, sampling_type="local", units='cm/s')
    temp_ds.add_field(("gas", "velocity_z"), function=velocity_z, sampling_type="local", units='cm/s')    
    temp_ds.add_field(("gas", "phase_types"), function=phase_types, sampling_type="local", units='')    

    data = {('gas','density'):(temp_ds.data['gas','density']),\
            ('gas','temperature'):(temp_ds.data['gas','temperature']),\
            ('gas','metallicity'):(temp_ds.data['gas','metallicity']),\
            ('gas','velocity_x'):(temp_ds.data['gas','velocity_x']),\
            ('gas','velocity_y'):(temp_ds.data['gas','velocity_y']),\
            ('gas','velocity_z'):(temp_ds.data['gas','velocity_z']),\
            ('gas','phase_types'):(temp_ds.data['gas','phase_types'])}
    bbox = np.array([[np.amin(temp_ds.data['data','x']),np.amax(temp_ds.data['data','x'])],
                     [np.amin(temp_ds.data['data','y']),np.amax(temp_ds.data['data','y'])],
                     [np.amin(temp_ds.data['data','z']),np.amax(temp_ds.data['data','z'])]])
    sim_time = 436117076640000000*1/(redshift+1)
    ds = yt.load_uniform_grid(data, temp_ds.data['gas','density'].shape, \
                              length_unit="kpc", bbox=bbox,sim_time = sim_time)
    ds.current_redshift = float(redshift)
    return ds
