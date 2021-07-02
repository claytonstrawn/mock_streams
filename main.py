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


def identify_phases():
    pass

#math section 
#code leader: Jewon
def create_fields():
    pass

#yt section 
#code leader: Vayun
def convert_to_dataset(fields): #'fields' has fields ordered with the following: densities, temperatures, metallicities.
    data = {('gas','density'):(fields[0], 'g*cm**(-3)'),('gas','temperature'):(fields[1],'K'),('gas','metallicity'):(fields[2],'Zsun')}
    bbox = np.array([[-max_size,max_size],[-max_size,max_size],[-max_size,max_size]])
    ds = yt.load_uniform_grid(data, densities.shape, length_unit="kpc", bbox=bbox)
    return ds