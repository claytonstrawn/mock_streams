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

def set_up_round_numbers(model):
    if model['box_size'] == 'Rvir':
        model['box_size'] = model['Rvir']*2
    model['Mvir'] = np.nan

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
    stream_width = {1:[Rs],2:[Rs]*2,3:[Rs]*3,4:[Rs]*4,5:[Rs]*5}
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

required_for_startup = {}
required_for_startup['round_numbers'] = ['Rvir','box_size']
required_for_startup['M20'] = ['Mvir','z','box_size','beta','s','eta','fh','ths','thh']

editable_not_required = {}
editable_not_required['round_numbers'] = ['z','beta','n','interface_thickness','stream_metallicity',\
                             'interface_metallicity','bulk_metallicity','stream_rotation',\
                             'endpoint','dist_method','n_streams','startpoint',\
                             'stream_size_growth','stream_width','stream_temperature',\
                             'bulk_temperature','stream_density','bulk_density']
editable_not_required['M20'] = ['n','interface_thickness','stream_metallicity',\
                             'interface_metallicity','bulk_metallicity','stream_rotation',\
                             'endpoint','dist_method','n_streams']

non_editable_fixed = {}
non_editable_fixed['round_numbers'] = ['density_contrast','Mvir']
non_editable_fixed['M20'] = ['Rvir','a','stream_size_growth','stream_width','density_contrast','stream_temperature',\
                          'bulk_temperature','stream_density','bulk_density']

calculate_fixed_params = {}
calculate_fixed_params['round_numbers'] = set_up_round_numbers
calculate_fixed_params['M20'] = set_up_M20


def all_lists_disjoint(a,b,c):
    overlap = (set(a)&set(b))|((set(a)|set(b))&set(c))
    return overlap
    

for model_name in ['round_numbers','M20']:
    overlap = all_lists_disjoint(required_for_startup[model_name],
                                 editable_not_required[model_name],
                                 non_editable_fixed[model_name])
    assert not overlap, 'parameters "%s" repeat in multiple lists under model %s!'%(overlap,model_name)