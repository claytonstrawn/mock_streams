import numpy as np
import yt
import trident
import mock_streams.defaults

def main_function(geo_args, phys_args):
    background_grid,Rvir = do_setup()
    phase_grid = identify_phases(background_grid, geo_args)
    fields = create_fields(background_grid, phase_grid, phys_args, Rvir)
    ds = convert_to_dataset(fields)
    return ds

def do_setup(Rvir,n=50,box_size = 200):
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
a = 0
b = 0
c = 0
d = 0
e = 100
f = 0

#defines the x,y,and z coordinates
def throughline(r):
    x = (d-a)*r + a
    y = (e-b)*r + b
    z = (f-c)*r + c
    return x,y,z

def distance_to_line(x,y,z,linex,liney,linez):
    #x is a number between 0 and 1
    #y is a number between 0 and 1
    #z is a number between 0 and 1
    #linex,liney,linez are arrays outputed from throughline
    distances = np.zeros(len(linex))
    for i in range(len(linex)):
        xpos = linex[i]
        ypos = liney[i]
        zpos = linez[i]
        dx = (xpos-x)**2
        dy = (ypos-y)**2
        dz = (zpos-z)**2
        distance = np.sqrt(dx+dy+dz)
        distances[i] = distance
    return np.amin(distances)

#Measures the distance from a random point to the line calculate above
def field_distance_to_line(xs,ys,zs,linex,liney,linez):
    all_distances = xs*0.0
    for i in range(len(xs)):
        for j in range(len(xs[i])):
            for k in range(len(xs[i,j])):
                all_distances[i,j,k] = distance_to_line(xs[i,j,k],ys[i,j,k],zs[i,j,k],linex,liney,linez)
    return all_distances

#Assigns a number to the distances of random numbers which determines whether 
#they are in the stream,interface or bulk.
def distance_check(xs,ys,zs,linex,liney,linez):
    all_distances = field_distance_to_line(xs,ys,zs,linex,liney,linez)
    phase_types = xs*0.0
    for i in range(len(xs)):
        for j in range(len(xs[i])):
            for k in range(len(xs[i,j])):
                if all_distances[i,j,k] < 30:
                    phase_types[i,j,k] = 1
                elif 30 < all_distances[i,j,k] < 40:
                    phase_types[i,j,k] = 2
                else:
                    phase_types[i,j,k] = 3
    return phase_types

def identify_phases(xs,ys,zs):
    linex,liney,linez = throughline(np.linspace(0,1,30))
    phase_types = distance_check(xs,ys,zs,linex,liney,linez)
    return phase_types

#math section 
#code leader: Jewon

def temperature_field(phase_types):
    temperature = np.zeros((n, n, n))
    temperature[phase_types == 1] = mock_streams.defaults.temperature_1
    temperature[phase_types == 2] = mock_streams.defaults.temperature_2
    temperature[phase_types == 3] = mock_streams.defaults.temperature_3
    return temperature

def density_field(background_grid, phase_types):
    xs = background_grid[0]
    ys = background_grid[1]
    zs = background_grid[2]

    rho_0 = np.zeros((n, n, n))
    rs = np.sqrt(xs**2+ys**2+zs**2)
    beta = mock_streams.defaults.beta

    rho_0[phase_types == 1] = mock_streams.defaults.rho_0_1
    rho_0[phase_types == 2] = mock_streams.defaults.rho_0_2
    rho_0[phase_types == 3] = mock_streams.defaults.rho_0_1
    
    density = rho_0 * (rs/Rvir)**beta
    return density

def metallicity_field(phase_types):
    metallicity = np.zeros((n, n, n))
    metallicity[phase_types == 1] = mock_streams.defaults.metallicity_1
    metallicity[phase_types == 2] = mock_streams.defaults.metallicity_2
    metallicity[phase_types == 3] = mock_streams.defaults.metallicity_3
    return metallicity

def create_fields(background_grid, phase_types, phys_args, Rvir):
    fields = []
    fields.append(density_field(background_grid, phase_types))
    fields.append(temperature_field(phase_types))
    fields.append(metallicity_field(phase_types))
    return fields

#yt section 
#code leader: Vayun
def convert_to_dataset(fields): #assuming that the 'fields' parameter has fields ordered with the following: densities, temperatures, metallicities.
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
