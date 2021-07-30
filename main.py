import numpy as np
import yt
from unyt import mh
import trident
from mock_streams import geometry,math,defaults,ytinterface,model_setup
from mock_streams import __version__
import datetime
import os

def create_mock(model_name = 'round_numbers',listargs = False,write_metadata = False,\
                filename = 'mock.h5',return_model = False,**kwargs):
    if listargs:
        model_setup.describe_model(model_name)
        return
    model = model_setup.set_up_model(kwargs,model_name)
    background_grid = do_setup(model)
    phase_grid = identify_phases(background_grid, model)
    fields = create_fields(background_grid, phase_grid, model)
    filename = convert_to_dataset(fields,filename)
    ds = load_dataset(filename,model=model)
    if write_metadata:
        if write_metadata is True:
            simnum = '00'
        else:
            simnum = '%02d'%write_metadata
        write_metadata_for_quasarscan(filename,'MOCK_v1_mockstreams_%s'%simnum,model)
        print('loaded dataset MOCK_v1_mockstreams_%s, using model "%s" at redshift %.2f'%\
              (simnum,model_name,ds.current_redshift))
    else:
        print('loaded dataset using model "%s" at redshift %.2f'%(model_name,ds.current_redshift))
    if return_model:
        return ds,model
    else:
        return ds

def turn_off_yt_comments():
    yt.funcs.mylog.setLevel(50)

def do_setup(model):
    max_size = model['box_size']/2
    n = model['n']
    
    x_vals = np.linspace(-max_size,max_size,n)
    y_vals = np.linspace(-max_size,max_size,n)
    z_vals = np.linspace(-max_size,max_size,n)

    xs = np.tile(x_vals,(n,n,1)).transpose((2,1,0))
    ys = np.tile(y_vals,(n,n,1)).transpose((0,1,2))
    zs = np.tile(z_vals,(n,n,1)).transpose((1,2,0))
    return (xs,ys,zs)

#geometry section 
#code leader: Parsa
def identify_phases(background_grid, model):
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
    return geometry.identify_phases(background_grid,model).transpose((0,2,1))

#math section 
#code leader: Jewon
def create_fields(background_grid, phase_types, model):
    #phys_args options:
    #density_contrast = 1 -> no difference b/w stream and bulk, rho_s/rho_b = 1
    #density_contrast = 10 -> rho_s/rho_b = 10
    #beta = -1.5 -> all three components follow same powerlaw of rho_0 * (r/Rvir)**-1.5
    #beta = (-1.5,-2.5) -> stream,bulk follow different powerlaws of rho_0 * (r/Rvir)**-1.5 and -2.5, respectively
    #metallicity_growth = 0 -> stream, bulk, interface all constant metallicity from defaults
    #metallicity_growth = -1 -> stream metallicity increases closer to center at Z_0 *(r/Rvir)**-1
    #temperatures = 'constant' -> keep temperature constant inside the structure
    
    fields = {}
    fields['density']=math.density_field(background_grid, phase_types, model)*mh.in_units('g')
    fields['temperature']=math.temperature_field(background_grid, phase_types, model)
    fields['metallicity']=math.metallicity_field(background_grid, phase_types, model)
    velocity=math.velocity_field(background_grid, phase_types, model)
    fields['velocity_x']=velocity[0]
    fields['velocity_y']=velocity[1]
    fields['velocity_z']=velocity[2]
    fields['xs'] = background_grid[0]
    fields['ys'] = background_grid[1]
    fields['zs'] = background_grid[2]
    fields['phase_types'] = phase_types
    return fields

#yt section 
#code leader: Vayun
def convert_to_dataset(fields,filename): 
    #assuming that the 'fields' parameter has fields ordered with the following: densities, temperatures, metallicities.
    return ytinterface.create_dataset(fields, filename)
   
def load_dataset(filename,model=None,redshift=None):
    if not redshift:
        redshift = model['z']
    return ytinterface.load_ds(filename,redshift)

def write_metadata_for_quasarscan(filename,fullname,model):    
    pathname = os.path.expanduser('~/quasarscan_data/galaxy_catalogs/%s'%fullname)
    if not os.path.exists(pathname):
        os.mkdir(pathname)
    z = model['z']
    a = 1.0/(1.0+z)
    Mvir = model['Mvir']
    Rvir = model['Rvir']
    center_x, center_y, center_z = 0.0,0.0,0.0
    L_x, L_y, L_z = 0,0,1
    all_lines = ["Metadata recorded on file %s with mockstreams version %s on date %s"%\
                 (filename,__version__,str(datetime.datetime.now()))]
    headers = ['a','Rvir','center_x', 'center_y', 'center_z', 'L_x', 'L_y', 'L_z']
    for quantity in model.keys():
        model_type = type(model[quantity])
        if model_type not in [str,int,float]:
            continue
        if quantity not in headers:
            headers.append(quantity)
    all_lines.append(str(headers)[1:-1].replace("'",""))
    current_line = ''
    for quantity in headers:
        try:
            to_write = eval(quantity)
        except:
            to_write = model[quantity]
        current_line += '%s, '%to_write
    all_lines.append(current_line[:-2])
    if os.path.exists(os.path.join(pathname,fullname+'_metadata.txt')):
        print('warning: overriding existing metadata file! Old quasarspheres at different redshifts will not be read correctly.')
    
    with open(os.path.join(pathname,fullname+'_metadata.txt'),'w') as f:
        for line in all_lines:
            f.write(line+'\n')