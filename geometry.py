import numpy as np

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

def min_distance_check(xs,ys,zs,throughline,model,n_line_points = 30):
    startpoint = model['startpoint']
    n_streams = model['n_streams']
    endpoints = get_multiple_endpoints(model)
    Rvir = model['Rvir']
    interface_thickness = model['interface_thickness']
    stream_width = model['stream_width']
    if isinstance(stream_width,dict):
        stream_width = stream_width[n_streams]
    elif not isinstance(stream_width,list):
        stream_width = [stream_width]*n_streams
    elif isinstance(stream_width,list):
        assert len(stream_width) == n_streams
    if n_streams > 1:
        assert isinstance(stream_width,list) and len(stream_width) == n_streams,(stream_width,n_streams)
        np.random.shuffle(stream_width)
    else:
        stream_width = [stream_width]

    for i,endpoint in enumerate(endpoints):
        linex,liney,linez = throughline(startpoint,endpoint,Rvir,model)(np.linspace(0,1,n_line_points))
        all_distances = distance_to_line(xs,ys,zs,linex,liney,linez)
        phase_types = xs*0.0
        stream_mask = all_distances < stream_width[i]
        phase_types[stream_mask] = 1
            
        interface_mask = np.logical_and.reduce((stream_width[i]<=all_distances,
                                                all_distances<stream_width[i]+interface_thickness,
                                                phase_types == 0))
        phase_types[interface_mask] = 2
    phase_types[phase_types==0] = 3
    return phase_types


def spiral_throughline(startpoint,endpoint,Rvir,model):
    b = model['stream_rotation']
    x1,y1,z1 = startpoint
    x2,y2,z2 = endpoint
    def spiral_throughline_helper(t):
        theta2 = np.arccos(x2/Rvir)
        if y2<0:
            theta2 = -theta2
        x = t*Rvir*np.cos((t-1)*b*(2*np.pi)+theta2)
        y = t*Rvir*np.sin((t-1)*b*(2*np.pi)+theta2)
        z = (z2-z1)*t + z1
        return np.array([x,y,z])
    return spiral_throughline_helper

def straight_throughline(startpoint,endpoint,Rvir,model):
    x1,y1,z1 = startpoint
    x2,y2,z2 = endpoint
    def straight_throughline_helper(r):
        x = (x2-x1)*r + x1
        y = (y2-y1)*r + y1
        z = (z2-z1)*r + z1
        return np.array([x,y,z])
    return straight_throughline_helper

def acceptable_distance(stream_width,stream_size_growth):
    def acceptable_distance_helper(r):
        return stream_width*r**stream_size_growth
    return acceptable_distance_helper

def get_multiple_endpoints(model,random_spread = 1.0,off_plane_spread = 1.0):
    n = model['n_streams']
    Rvir = model['Rvir']
    first_endpoint = model['endpoint']
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
        

def radial_distance_check(xs,ys,zs,throughline,model):
    Rvir = model['Rvir']
    n_streams = model['n_streams']
    stream_width = model['stream_width']
    if isinstance(stream_width,dict):
        stream_width = stream_width[n_streams]
    elif not isinstance(stream_width,list):
        stream_width = [stream_width]*n_streams
    elif isinstance(stream_width,list):
        assert len(stream_width) == n_streams
    startpoint = model['startpoint']
    endpoints = get_multiple_endpoints(model)
    interface_thickness = model['interface_thickness']
    stream_size_growth = model['stream_size_growth']
    if n_streams > 1:
        assert isinstance(stream_width,list) and len(stream_width) == n_streams
        np.random.shuffle(stream_width)
    else:
        stream_width = [stream_width]
    
    phase_types = xs*0.0
    rs = np.sqrt(xs**2+ys**2+zs**2)
    
    for i in range(n_streams):
        endpoint = endpoints[i]
        x_line,y_line,z_line = throughline(startpoint,endpoint,Rvir,model)(rs/Rvir)
        distance = np.sqrt((xs-x_line)**2+(ys-y_line)**2+(zs-z_line)**2)
        stream_distance = acceptable_distance(stream_width[i],stream_size_growth)(rs/Rvir)
    
        stream_mask = distance<stream_distance
        phase_types[stream_mask] = 1
    
        interface_mask = np.logical_and.reduce((stream_distance <= distance, 
                                    distance < stream_distance + interface_thickness,
                                    phase_types == 0))
        phase_types[interface_mask] = 2
    
    bulk_mask = (phase_types==0)
    phase_types[bulk_mask] = 3
    
    return phase_types

def slab_distance_check(xs,ys,zs,throughline,model,n_t = 60):
    Rvir = model['Rvir']
    b = model['stream_rotation']
    n_streams = model['n_streams']
    stream_width = model['stream_width']
    if isinstance(stream_width,dict):
        stream_width = stream_width[n_streams]
    elif not isinstance(stream_width,list):
        stream_width = [stream_width]*n_streams
    elif isinstance(stream_width,list):
        assert len(stream_width) == n_streams
    startpoint = model['startpoint']
    endpoints = get_multiple_endpoints(model)
    interface_thickness = model['interface_thickness']
    stream_size_growth = model['stream_size_growth']
    if n_streams > 1:
        assert isinstance(stream_width,list) and len(stream_width) == n_streams
        np.random.shuffle(stream_width)
    else:
        stream_width = [stream_width]
        
    phase_types = (xs*0).astype(int)
    ts = np.linspace(0,max(2,6*b),n_t)
    for i in range(n_streams):
        p = throughline((0,0,0),endpoints[i],Rvir,model)(ts)
        Rs = acceptable_distance(stream_width[i],stream_size_growth)(ts)
        for j in range(len(ts)-2):
            p1,p2,R1,R2 = p[:,j],p[:,j+2],Rs[j],Rs[j+2]
            w = np.linalg.norm(p2-p1)
            A,B,C = (p2-p1)/w
            x0,y0,z0 = (p1+p2)/2
            D = -A*x0-B*y0-C*z0
            d = np.abs(A*xs+B*ys+C*zs+D)
            slab = (d<=w/2)
            d1_sq = (xs[slab]-p1[0])**2+(ys[slab]-p1[1])**2+(zs[slab]-p1[2])**2
            d2_sq = (xs[slab]-p2[0])**2+(ys[slab]-p2[1])**2+(zs[slab]-p2[2])**2
            a1 = w/2+(d1_sq - d2_sq)/(2*w)
            h = np.sqrt(d1_sq-a1**2)
            R = R1+(R2-R1)/w*a1
            stream = (h<R)
            interface = np.logical_and.reduce((h>=R,h<R+interface_thickness,
                                    phase_types[slab] == 0))
            phase_types.flat[np.flatnonzero(slab)[stream]] = 1
            phase_types.flat[np.flatnonzero(slab)[interface]] = 2
    bulk = (phase_types==0)
    phase_types[bulk] = 3
    return phase_types


def identify_phases(background_grid,model):
    stream_rotation = model['stream_rotation']
    dist_method = model['dist_method']

    if stream_rotation == 0:
        throughline = straight_throughline
    else:
        throughline = spiral_throughline
    
    if dist_method == 'min':
        distance_check = min_distance_check
    elif dist_method == 'radial':
        distance_check = radial_distance_check
    elif dist_method == 'slab':
        distance_check = slab_distance_check
    else:
        assert False, 'Not implemented'
        
    xs,ys,zs = background_grid
    return distance_check(xs,ys,zs,throughline,model)
