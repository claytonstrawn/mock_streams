def main_function(geo_args, phys_args):
    background_grid = do_setup()
    phase_grid = geometry.identify_phases(background_grid, geo_args)
    fields = math.create_fields(background_grid, phase_grid, phys_args)
    ds = yt_section.convert_to_dataset(fields)
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
