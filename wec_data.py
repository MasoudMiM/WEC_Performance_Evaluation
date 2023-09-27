import numpy as np

# import wec_data from https://mhkdr.openei.org/submissions/380

def importing_json_file(url_input):
    # this function imports a json file from a url
    import requests
    import json
    url = url_input
    response = requests.get(url)
    data = response.json()
    return data

# - McCabe Wave Pump (attenuator wec)
dic_mccabe_wave_pump = {}
dic_mccabe_wave_pump['McCabe_Wave_Pump_Model_Size_1'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/mccabe_data_2.5m.mat.json')
dic_mccabe_wave_pump['McCabe_Wave_Pump_Model_Size_2'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/mccabe_data_5m.mat.json')
dic_mccabe_wave_pump['McCabe_Wave_Pump_Model_Size_3'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/mccabe_data_10m.mat.json')
dic_mccabe_wave_pump['McCabe_Wave_Pump_Model_Size_4'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/mccabe_data_14m.mat.json')
dic_mccabe_wave_pump['McCabe_Wave_Pump_Model_Size_5'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/mccabe_data_20m.mat.json')

print(dic_mccabe_wave_pump.keys())
print(len(dic_mccabe_wave_pump['McCabe_Wave_Pump_Model_Size_1']))
# convert the list into numpy 2d array

my_list = dic_mccabe_wave_pump['McCabe_Wave_Pump_Model_Size_1']
wec_type = my_list[20]['wec_type']
wec_scale = my_list[20]['wec_scale']
Tp_values = my_list[20]['peak_period_range']['value']
print(Tp_values)


