import numpy as np
import yt
from unyt import mh
import trident
from mock_streams import geometry,math,defaults,ytinterface
from mock_streams.defaults import lookup
from mock_streams import __version__
import datetime
import os

#from mock_streams import yt_interface

possible_setup_args = ['Rvir','Mvir','n','box_size','a','z']
possible_geo_args = ['stream_rotation','n_streams','stream_size_growth','stream_width','startpoint','endpoint','dist_method','interface_thickness']
possible_phys_args = ['density_contrast','beta','metallicity_growth','bulk_temperature']

def main_function(**kwargs):
    print('"main_function" is deprecated, please use "create_mock" instead. Will remove by end of week.\n')
    return create_mock(**kwargs)

def create_mock(setup_args=None,geo_args=None, phys_args=None,listargs = False,write_metadata = False,**kwargs):
    if listargs == True:
        print('Available keys are %s, %s, %s'%(possible_setup_args,possible_geo_args,possible_phys_args))
        return
    if setup_args is None:
        setup_args = {}
    if geo_args is None:
        geo_args = {}
    if phys_args is None:
        phys_args = {}
    for key in kwargs.keys():
        if key in possible_setup_args:
            setup_args[key] = kwargs[key]
        elif key in possible_geo_args:
            geo_args[key] = kwargs[key]
        elif key in possible_phys_args:
            phys_args[key] = kwargs[key]
        else:
            assert False,'Key "%s" not recognized! Available keys are %s, %s, %s'%(key, possible_setup_args, possible_geo_args, possible_phys_args)
    background_grid,Rvir,redshift = do_setup(setup_args)
    phase_grid = identify_phases(background_grid, geo_args,Rvir)
    fields = create_fields(background_grid, phase_grid, phys_args, Rvir)
    filename = convert_to_dataset(background_grid, fields)
    ds = load_dataset(filename,redshift)
    if write_metadata:
        if write_metadata is True:
            simnum = '00'
        else:
            simnum = '%02d'%write_metadata
        write_metadata_for_quasarscan(filename,'MOCK_v1_mockstreams_%s'%simnum,setup_args)
    print('loaded dataset MOCK_v1_mockstreams_%s at redshift %f'%(simnum,redshift))
    return ds


def do_setup(setup_args):
    max_size = lookup('box_size',setup_args)/2
    n = lookup('n',setup_args)
    x_vals = np.linspace(-max_size,max_size,n)
    y_vals = np.linspace(-max_size,max_size,n)
    z_vals = np.linspace(-max_size,max_size,n)

    xs = np.tile(x_vals,(n,n,1)).transpose((2,1,0))
    ys = np.tile(y_vals,(n,n,1)).transpose((0,1,2))
    zs = np.tile(z_vals,(n,n,1)).transpose((1,2,0))
    
    Rvir = lookup('Rvir',setup_args)
    a = lookup('a',setup_args)
    if a == 1.0:
        redshift = lookup('z',setup_args)
    else:
        redshift = 1./a-1.
    return (xs,ys,zs),Rvir,redshift

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
    return geometry.identify_phases(background_grid,geo_args,Rvir).transpose((0,2,1))

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
    fields['density']=math.density_field(background_grid, phase_types, phys_args, Rvir)*mh.in_units('g')
    fields['temperature']=math.temperature_field(background_grid, phase_types, phys_args)
    fields['metallicity']=math.metallicity_field(background_grid, phase_types, phys_args)
    velocity=math.velocity_field(background_grid, phase_types, Rvir)
    fields['velocity_x']=velocity[0]
    fields['velocity_y']=velocity[1]
    fields['velocity_z']=velocity[2]
    return fields

#yt section 
#code leader: Vayun
def convert_to_dataset(background_grid, fields,filename='mock.h5'): 
    #assuming that the 'fields' parameter has fields ordered with the following: densities, temperatures, metallicities.
    return ytinterface.create_dataset(background_grid, fields, filename)
   
def load_dataset(filename,redshift):
    return ytinterface.load_ds(filename,redshift)

def write_metadata_for_quasarscan(filename,fullname,setup_args,tolerance = .001):    
    pathname = os.path.expanduser('~/quasarscan_data/galaxy_catalogs/%s'%fullname)
    if not os.path.exists(pathname):
        os.mkdir(pathname)
    a = lookup('a',setup_args)
    Mvir = lookup('Mvir',setup_args)
    Rvir = lookup('Rvir',setup_args)
    center_x, center_y, center_z = 0.0,0.0,0.0
    L_x, L_y, L_z = 0,0,1
    all_lines = ["Metadata recorded on file %s with mockstreams version %s on date %s"%\
                 (filename,__version__,str(datetime.datetime.now()))]
    all_lines.append(str(['a','Mvir','Rvir','center_x', 'center_y', 'center_z', 'L_x', 'L_y', 'L_z'])[1:-1].replace("'",""))
    
    current_line = ''
    for quantity in ['a','Mvir','Rvir','center_x', 'center_y', 'center_z', 'L_x', 'L_y', 'L_z']:
        to_write = eval(quantity)
        current_line += '%s, '%to_write
    all_lines.append(current_line[:-2])

    with open(os.path.join(pathname,fullname+'_metadata.txt'),'w') as f:
        for line in all_lines:
            f.write(line+'\n')