import numpy as np

def main_function(geo_args, phys_args):
    background_grid = do_setup()
    phase_types = identify_phases(background_grid, geo_args)
    fields = create_fields(background_grid, phase_grid, phys_args)
    ds = convert_to_dataset(fields)
    return ds

def do_setup(n=50,box_size = 200):
    max_size = box_size/2
    x_vals = np.linspace(-max_size,max_size,n)
    y_vals = np.linspace(-max_size,max_size,n)
    z_vals = np.linspace(-max_size,max_size,n)

    xs = np.tile(x_vals,(n,n,1)).transpose((2,1,0))
    ys = np.tile(y_vals,(n,n,1)).transpose((0,1,2))
    zs = np.tile(z_vals,(n,n,1)).transpose((1,2,0))
    return xs,ys,zs

def fake_phase_types(xs,ys,zs):
    streams = (xs>0)*(np.abs(ys)<20)*(np.abs(zs)<20)
    interfaces = np.logical_xor((xs>0)*(np.abs(ys)<30)*(np.abs(zs)<30),streams)
    bulk = np.logical_not(np.logical_or(streams,interfaces))
    phase_types = xs*0.0
    phase_types[streams] = 1
    phase_types[interfaces] = 2
    phase_types[bulk] = 3
    return phase_types

#geometry section 
#code leader: Parsa
def identify_phases():
    pass

#math section 
#code leader: Jewon
def create_fields():
    pass

#yt section 
#code leader: Vayun
def convert_to_dataset():
    pass
