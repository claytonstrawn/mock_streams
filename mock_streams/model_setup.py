import numpy as np
from unyt import mh
from mock_streams.defaults import lookup
    
class NonEditableValueError(Exception):
    def __init__(self, message):
        self.message = message
        print(self.message)
        
class UnknownValueError(Exception):
    def __init__(self, message):
        self.message = message
        print(self.message)

#default setup arguments
def set_up_model(start_up_dict,model_name):
    for key in start_up_dict.keys():
        if key in required_for_startup[model_name]:
            pass
        elif key in editable_not_required[model_name]:
            pass
        elif key in non_editable_fixed[model_name]:
            raise NonEditableValueError('key "%s" is not editable under model "%s"'%(key,model_name))
        else:
            raise UnknownValueError('key "%s" is not recognized in model "%s"'%(key,model_name))
    model = {'model_name':model_name}
    for key in required_for_startup[model_name]:
        model[key] = lookup(key,start_up_dict)
    calculate_fixed_params[model_name](model)
    for key in editable_not_required[model_name]:
        model[key] = lookup(key,start_up_dict)
    return model

def describe_model(model_name):
    print('model "%s" uses parameters %s and accepts parameters %s. It returns (non-editable) parameters %s.'%\
              (model_name,required_for_startup[model_name],\
               editable_not_required[model_name],non_editable_fixed[model_name]))
    
def explain_model(model):
    for key in model.keys():
        if key in explanations.keys():
            print(key,":",explanations[key])
        else:
            print(key,":",model[key])

def set_up_round_numbers(model):
    if model['box_size'] == 'Rvir':
        model['box_size'] = model['Rvir']*2
    elif model['box_size'] == '2Rvir':
        model['box_size'] = model['Rvir']*4
    model['Mvir'] = np.nan

    model['stream_density_beta'] = model['beta']
    model['bulk_density_beta'] = model['beta']
    model['stream_temperature_beta'] = 0
    model['bulk_temperature_beta'] = 0
    model['stream_metallicity_beta'] = 0
    model['interface_metallicity_beta'] = 0
    model['bulk_metallicity_beta'] = 0

def set_up_M20(model):
    Mvir = model['Mvir']
    z = model['z']
    beta = model['beta']
    s = model['s']
    eta = model['eta']
    fh = model['fh']
    ths = model['ths']
    thh = model['thh']
    
    oneplusz3 = (1+z)/3
    M12 = Mvir/1e12
    Rvir = 100*M12**(1/3)*oneplusz3**(-1)
    delta = 100*M12**(2/3)*oneplusz3*thh/ths
    delta100 = delta/100
    Rs = Rvir*0.16*oneplusz3**(0.5)*delta100**(-0.5)*s/(eta*fh)
    rho_0s = 1.1e-26/mh.in_units('g').v*oneplusz3**3*delta100*fh
    Tvir = 1.5e6*M12**(2/3)*oneplusz3
    stream_temperature = ths*1.5e4
    bulk_temperature = thh*Tvir
    stream_density = rho_0s
    bulk_density = rho_0s/delta
    stream_width = {1:[Rs],2:[Rs]*2,3:[Rs]*3,4:[Rs]*4}
    stream_size_growth = beta/2

    #determined by above, do not overwrite
    model['Rvir'] = Rvir
    model['density_contrast'] = delta
    model['stream_temperature'] = stream_temperature
    model['bulk_temperature'] = bulk_temperature
    model['stream_density'] = stream_density
    model['bulk_density'] = bulk_density
    model['stream_width'] = stream_width
    model['stream_size_growth'] = stream_size_growth
    #startpoint required to be at center
    model['startpoint'] = [0,0,0] #center of simulation
    model['a'] = 1.0/(1.0+z) #expansion_parameter
    if model['box_size'] == 'Rvir':
        model['box_size'] = model['Rvir']*2
    elif model['box_size'] == '2Rvir':
        model['box_size'] = model['Rvir']*4
    else:
        print(model['box_size'])

    model['stream_density_beta'] = model['beta']
    model['bulk_density_beta'] = model['beta']
    model['stream_temperature_beta'] = 0
    model['bulk_temperature_beta'] = 0
    model['stream_metallicity_beta'] = 0
    model['interface_metallicity_beta'] = 0
    model['bulk_metallicity_beta'] = 0

def set_up_vela(model):
    if model['box_size'] == 'Rvir':
        model['box_size'] = model['Rvir']*2
    elif model['box_size'] == '2Rvir':
        model['box_size'] = model['Rvir']*4
    model['Mvir'] = np.nan
    model['stream_temperature'] = model['vela_stream_temperature_Rvir']
    model['bulk_temperature'] = model['vela_bulk_temperature_Rvir']
    model['stream_density'] = model['vela_stream_density_Rvir']
    model['bulk_density'] = model['vela_bulk_density_Rvir']
    model['stream_metallicity'] = model['vela_stream_metallicity_Rvir']
    model['interface_metallicity'] = model['vela_interface_metallicity_Rvir']
    model['bulk_metallicity'] = model['vela_bulk_metallicity_Rvir']

required_for_startup = {}
required_for_startup['round_numbers'] = ['Rvir','box_size','beta']
required_for_startup['M20'] = ['Mvir','z','box_size','beta','s','eta','fh','ths','thh']
required_for_startup['vela'] = ['Rvir','box_size','vela_stream_temperature_Rvir','vela_bulk_temperature_Rvir',\
                                'vela_stream_density_Rvir','vela_bulk_density_Rvir','vela_stream_metallicity_Rvir',\
                                'vela_interface_metallicity_Rvir','vela_bulk_metallicity_Rvir']

editable_not_required = {}
editable_not_required['round_numbers'] = ['z','n','interface_thickness','stream_metallicity',\
                             'interface_metallicity','bulk_metallicity','stream_rotation',\
                             'endpoint','dist_method','n_streams','startpoint',\
                             'stream_size_growth','stream_width','stream_temperature',\
                             'bulk_temperature','stream_density','bulk_density']
editable_not_required['M20'] = ['n','interface_thickness','stream_metallicity',\
                             'interface_metallicity','bulk_metallicity','stream_rotation',\
                             'endpoint','dist_method','n_streams']
editable_not_required['vela'] = ['z','stream_density_beta','bulk_density_beta','stream_temperature_beta',\
                                'bulk_temperature_beta','stream_metallicity_beta','interface_metallicity_beta',\
                                'bulk_metallicity_beta','n','interface_thickness','stream_rotation',\
                             'endpoint','dist_method','n_streams','startpoint',\
                             'stream_size_growth','stream_width']

non_editable_fixed = {}
non_editable_fixed['round_numbers'] = ['density_contrast','Mvir',\
                                'stream_density_beta','bulk_density_beta','stream_temperature_beta',\
                                'bulk_temperature_beta','stream_metallicity_beta','interface_metallicity_beta',\
                                'bulk_metallicity_beta']
non_editable_fixed['M20'] = ['Rvir','a','stream_size_growth','stream_width','density_contrast',\
                            'stream_temperature','bulk_temperature','stream_density','bulk_density'\
                            'stream_density_beta','bulk_density_beta','stream_temperature_beta',\
                                'bulk_temperature_beta','stream_metallicity_beta','interface_metallicity_beta',\
                                'bulk_metallicity_beta']
non_editable_fixed['vela'] = ['stream_temperature','stream_metallicity',\
                             'interface_metallicity','bulk_metallicity',
                             'bulk_temperature','stream_density','bulk_density']

calculate_fixed_params = {}
calculate_fixed_params['round_numbers'] = set_up_round_numbers
calculate_fixed_params['M20'] = set_up_M20
calculate_fixed_params['vela'] = set_up_vela


def all_lists_disjoint(a,b,c):
    overlap = (set(a)&set(b))|((set(a)|set(b))&set(c))
    return overlap
    
explanations = {'Rvir':'(kpc), virial radius',
                'box_size':'(kpc), width of mock region, default:"Rvir"',
                'Mvir':'(Msun), Virial mass, or total halo mass. default:%s, range:[10^11-10^13]'%lookup('Mvir'),
                'z':'(unitless), redshift, default:%s, range:[1-4]'%lookup('z'),
                'beta':'(unitless) powerlaw controlling bulk density growth, default:%s, range:[1-3]'%lookup('beta'),
                's':'(unitless) normalized "amount" of gas flowing in along each stream, default:'+
                    '%s, range:[0.3-3.0].(had a tilde over s in M20)'%lookup('s'),
                'eta':'(unitless) normalized speed of streams w.r.t. Vvir, default:'
                    '%s, range:[0.5-sqrt(2)]'%lookup('eta'), 
                'fh':'(unitless) normalized "amount" of gas in hot medium at Rvir, default:'
                    '%s, range:[1.0-3.0] (had a tilde over fh in M20)'%lookup('fh'),
                'ths':'(unitless) normalized temperature of gas in stream w.r.t 1.5e4 K (cooling peak), default:'
                    '%s, range:[0.5-2.0]'%lookup('ths'),
                'thh':'(unitless) normalized temperature of gas in stream w.r.t Tvir, default:'
                    '%s, range:[0.5-2.0]'%lookup('thh'),
                'n':'(unitless) number grid resolution elements in each direction, default:%s.'%lookup('n')+
                    'higher n means slower mock but better data',
                'interface_thickness':'(kpc) overall (constant) interface thickness, default:'+
                    '%s.'%lookup('interface_thickness'),
                'stream_metallicity':'(Zsun) overall (constant) metallicity of the streams, default:'+
                    '%s.'%lookup('stream_metallicity'),\
                'interface_metallicity':'(Zsun) overall (constant) metallicity of the interface, default:'+
                    '%s.'%lookup('interface_metallicity'),\
                'bulk_metallicity':'(Zsun) overall (constant) metallicity of the bulk, default:'+
                    '%s.'%lookup('bulk_metallicity'),\
                'stream_rotation':'amount of rotation of the streams. The stream throughline is defined'+
                    'to be an Archimedean spiral, and is scaled so that stream_rotation = 1 means making'+
                    'one full rotation. default: %s, range [0.0-0.4]'%lookup('stream_rotation'),\
                'endpoint':'(kpc) 3D location of point where stream interects virial radius sphere, '+
                    'default is "random", which will put point anywhere near xy plane. Other streams are '+
                    'designed to be semi-equally spaced in azimuthal angle.',
                'dist_method':'(string) Method of determining distance to stream throughline, affecting'+
                    'stream width. Default: %s, recommend "slab" if stream_rotation > 0'%lookup('dist_method'),
                'n_streams':'(int) Number of streams generated, equally spaced in angle default: '+
                    '%s, range = [1-4]'%lookup('n_streams'),
                'startpoint':'(kpc) Origin of streams. Some models require the center of the virial radius.'+
                    ' default: %s'%lookup('startpoint'),
                'stream_size_growth':'(unitless) powerlaw regulating size of streams as function of radius.'+
                    '(streams are smaller on the inner halo). default: %s'%lookup('stream_size_growth'),
                'stream_width':'(dict of lists of kpc) Size the streams reach at Rvir (according to dist_method).'+
                    ' Is a dictionary to include results for n_streams in [1-4]. default: %s'%lookup('n_streams'),
                'stream_temperature':'(K) Overall temperature of streams, constant for now. '+
                    'default: %s'%lookup('stream_temperature'),
                'bulk_temperature':'(K) Overall temperature of bulk, constant for now. '+
                    'default: %s'%lookup('bulk_temperature'),
                'stream_density':'(cm^-3) Density of stream at Rvir, will increase as approach galaxy '+
                    'default: %s'%lookup('stream_density'),
                'bulk_density':'(cm^-3) Density of bulk at Rvir, will increase as approach galaxy '+
                    'default: %s'%lookup('bulk_density'),}

for model_name in ['round_numbers','M20']:
    overlap = all_lists_disjoint(required_for_startup[model_name],
                                 editable_not_required[model_name],
                                 non_editable_fixed[model_name])
    assert not overlap, 'parameters "%s" repeat in multiple lists under model %s!'%(overlap,model_name)

   

