import numpy as np
import mock_streams.defaults

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


def field_distance_to_line(xs,ys,zs,linex,liney,linez):
    all_distances = xs*0.0
    for i in range(len(xs)):
        for j in range(len(xs[i])):
            for k in range(len(xs[i,j])):
                all_distances[i,j,k] = distance_to_line(xs[i,j,k],ys[i,j,k],zs[i,j,k],linex,liney,linez)
    return all_distances


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


def throughline(r,Rvir):
    theta = np.random.random()*2*np.pi
    x2 = Rvir*np.cos(theta)
    y2 = Rvir*np.cos(theta)
    z2 = 0
    x = (x2-mock_streams.defaults.x1)*r + mock_streams.defaults.x1
    y = (y2-mock_streams.defaults.y1)*r + mock_streams.defaults.y1
    z = (z2-mock_streams.defaults.z1)*r + mock_streams.defaults.z1
    return x,y,z


def acceptable_distance(r):
    return mock_streams.defaults.stream_radius_at_Rvir*r


def variable_distance_check(xs,ys,zs,Rvir):
    phase_types = xs*0.0
    rs = np.sqrt(xs**2+ys**2+zs**2)
    x_line,y_line,z_line = throughline(rs/100,Rvir)
    distance = np.sqrt((xs-x_line)**2+(ys-y_line)**2+(zs-z_line)**2)
    stream_distance = acceptable_distance(rs/100)
    
    stream_mask = distance<stream_distance
    phase_types[stream_mask] = 1
    
    interface_mask = np.logical_and(stream_distance < distance, 
                                    distance < stream_distance +   mock_streams.defaults.interface_thickness)
    phase_types[interface_mask] = 2
    
    bulk_mask = distance > stream_distance + mock_streams.defaults.interface_thickness
    phase_types[bulk_mask] = 3
    return phase_types