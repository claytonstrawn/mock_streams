import numpy as np
from mock_streams.defaults import lookup

def distance_to_line(x,y,z,linex,liney,linez):
    #x is a number between 0 and 1
    #y is a number between 0 and 1
    #z is a number between 0 and 1
    #linex,liney,linez are arrays outputed from throughline
    shape = len(linex),x.shape[0],x.shape[1],x.shape[2]
    distances = np.zeros(shape)
    for i in range(len(linex)):
        xpos = linex[i]
        ypos = liney[i]
        zpos = linez[i]
        dx = (xpos-x)**2
        dy = (ypos-y)**2
        dz = (zpos-z)**2
        distances[i] = np.sqrt(dx+dy+dz)
    return np.amin(distances,axis=0)

def min_distance_check(xs,ys,zs,throughline,geo_args,Rvir,n_line_points = 30):
    stream_width = lookup('stream_width',geo_args)
    endpoint = lookup('endpoint',geo_args)
    interface_thickness = lookup('interface_thickness',geo_args)
    linex,liney,linez = throughline(startpoint,endpoint,Rvir)(np.linspace(0,1,n_line_points))
    all_distances = distance_to_line(xs,ys,zs,linex,liney,linez)
    phase_types = xs*0.0
    phase_types[all_distances < stream_width] = 1
    phase_types[np.logical_and(stream_width<=all_distances,all_distances<stream_width+interface_thickness)] = 2
    phase_types[all_distances >= stream_width+interface_thickness] = 3
    return phase_types


def straight_throughline(startpoint,endpoint,Rvir):
    x1,y1,z1 = startpoint
    x2,y2,z2 = endpoint
    def straight_throughline_helper(r):
        x = (x2-x1)*r + x1
        y = (y2-y1)*r + y1
        z = (z2-z1)*r + z1
        return x,y,z
    return straight_throughline_helper


def acceptable_distance(stream_width,stream_size_growth):
    def acceptable_distance_helper(r):
        return stream_width*r**stream_size_growth
    return acceptable_distance_helper

def get_multiple_endpoints(n,geo_args,Rvir,random_spread = 1.0,off_plane_spread = 1.0):
    first_endpoint = lookup('endpoint',geo_args)
    if first_endpoint == 'random':
        theta = np.random.random()*2*np.pi
        x2 = Rvir*np.cos(theta)
        y2 = Rvir*np.sin(theta)
        z2 = Rvir*off_plane_spread/10
        first_endpoint = x2,y2,z2
    else:
        theta = np.arctan2(first_endpoint[0],first_endpoint[1])
    endpoints = [first_endpoint]
    angle_spread = 2*np.pi/n
    random_dist = (np.random.random(n)-0.5)*random_spread
    for i in range(1,n):
        theta_i = theta+i*angle_spread+random_dist[i]
        x2 = Rvir*np.cos(theta_i)
        y2 = Rvir*np.sin(theta_i)
        z2 = 0
        next_endpoint = x2,y2,z2
        endpoints.append(next_endpoint)
    return endpoints
        

def radial_distance_check(xs,ys,zs,throughline,geo_args,Rvir):
    n_streams = lookup('n_streams',geo_args)
    stream_width = lookup('stream_width',geo_args)
    if isinstance(stream_width,dict):
        stream_width = stream_width[n_streams]
    elif not isinstance(stream_width,list) and n_streams==1:
        stream_width = [stream_width]
    startpoint = lookup('startpoint',geo_args)
    endpoints = get_multiple_endpoints(n_streams,geo_args,Rvir)
    interface_thickness = lookup('interface_thickness',geo_args)
    stream_size_growth = lookup('stream_size_growth',geo_args)
    if n_streams > 1:
        assert isinstance(stream_width,list) and len(stream_width) == n_streams
        np.random.shuffle(stream_width)
    else:
        stream_width = [stream_width]
    phase_types = xs*0.0
    rs = np.sqrt(xs**2+ys**2+zs**2)
    
    for i in range(n_streams):
        endpoint = endpoints[i]
        x_line,y_line,z_line = throughline(startpoint,endpoint,Rvir)(rs/Rvir)
        distance = np.sqrt((xs-x_line)**2+(ys-y_line)**2+(zs-z_line)**2)
        stream_distance = acceptable_distance(stream_width[i],stream_size_growth)(rs/Rvir)
    
        stream_mask = distance<stream_distance
        phase_types[stream_mask] = 1
    
        interface_mask = np.logical_and(stream_distance <= distance, 
                                    distance < stream_distance + interface_thickness)
        phase_types[interface_mask] = 2
    
    bulk_mask = (phase_types==0)
    phase_types[bulk_mask] = 3
    
    return phase_types


def identify_phases(background_grid,geo_args,Rvir):
    stream_rotation = lookup('stream_rotation',geo_args)
    dist_method = lookup('dist_method',geo_args)

    if stream_rotation == 0:
        throughline = straight_throughline
    else:
        assert False, 'Not implemented'
    
    if dist_method == 'min':
        distance_check = min_distance_check
    elif dist_method == 'radial':
        distance_check = radial_distance_check
    else:
        assert False, 'Not implemented'
        
    xs,ys,zs = background_grid
    return distance_check(xs,ys,zs,throughline,geo_args,Rvir)
