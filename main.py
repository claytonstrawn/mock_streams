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
def convert_to_dataset(fields, bbox): #assuming that the 'fields' parameter has fields ordered with the following: densities, temperatures, metallicities.
    data = {('gas','density'):(fields[0], 'g*cm**(-3)'),('gas','temperature'):(fields[1],'K'),('gas','metallicity'):(fields[2],'Zsun')}
    bbox = np.array([[-max_size,max_size],[-max_size,max_size],[-max_size,max_size]])
    ds = yt.load_uniform_grid(data, densities.shape, length_unit="kpc", bbox=bbox)
    trident.add_ion_fields(ds, ions=['O VI'], ftype="gas")
