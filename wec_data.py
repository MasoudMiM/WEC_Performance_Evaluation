import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import griddata
import matplotlib.colors as mcolors

import requests
import json

# import wec_data from https://mhkdr.openei.org/submissions/380


def importing_json_file(url_input):
    # this function imports a json file from a url
    url = url_input
    response = requests.get(url)
    data = response.json()
    return data

# - McCabe Wave Pump (attenuator wec)
dic_wec_devices = {}
dic_wec_devices['McCabe_Wave_Pump_Model_Size_1'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/mccabe_data_2.5m.mat.json')
dic_wec_devices['McCabe_Wave_Pump_Model_Size_2'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/mccabe_data_5m.mat.json')
dic_wec_devices['McCabe_Wave_Pump_Model_Size_3'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/mccabe_data_10m.mat.json')
dic_wec_devices['McCabe_Wave_Pump_Model_Size_4'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/mccabe_data_14m.mat.json')
dic_wec_devices['McCabe_Wave_Pump_Model_Size_5'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/mccabe_data_20m.mat.json')

# - OSWEC (oscillating water column wec)
dic_wec_devices['OSWEC_Model_Size_2'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/oswec_data_2m.mat.json')
dic_wec_devices['OSWEC_Model_Size_3'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/oswec_data_3m.mat.json')
dic_wec_devices['OSWEC_Model_Size_4'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/oswec_data_4m.mat.json')
dic_wec_devices['OSWEC_Model_Size_5'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/oswec_data_5m.mat.json')
dic_wec_devices['OSWEC_Model_Size_6'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/oswec_data_6m.mat.json')
dic_wec_devices['OSWEC_Model_Size_7'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/oswec_data_7m.mat.json')
dic_wec_devices['OSWEC_Model_Size_8'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/oswec_data_8m.mat.json')
dic_wec_devices['OSWEC_Model_Size_9'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/oswec_data_9m.mat.json')

# - Point Absorber - Single Body 
dic_wec_devices['Point_Absorber_Model_Size_2'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/point_a_data_2m.json')
dic_wec_devices['Point_Absorber_Model_Size_3'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/point_a_data_3m.json')
dic_wec_devices['Point_Absorber_Model_Size_4'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/point_a_data_4m.json')
dic_wec_devices['Point_Absorber_Model_Size_5'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/point_a_data_5m.json')
dic_wec_devices['Point_Absorber_Model_Size_6'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/point_a_data_6m.json')

# - Point Absorber - Two Body (RM3)
dic_wec_devices['Point_Absorber_Two_Body_Model_Size_2'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/rm3_data_2m%20(1).json')

dic_wec_devices['Point_Absorber_Two_Body_Model_Size_3'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/rm3_data_3m%20(1).json')
dic_wec_devices['Point_Absorber_Two_Body_Model_Size_4'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/rm3_data_4m%20(1).json')
dic_wec_devices['Point_Absorber_Two_Body_Model_Size_5'] = \
    importing_json_file('https://mhkdr.openei.org/files/380/rm3_data_5m%20(1).json')

# saving the dictionary as a json file
with open('wec_devices_data_links.json', 'w') as fp:
    json.dump(dic_wec_devices, fp)


plot_power = True

# looking at the json files, the wave height, wave period, and other data are stored in
# dictionaries that are specific items (starting from item 20 and increasing every 19 steps) 
# in a general list. The following code extracts the wave height and wave period data 
# for each wec size and stores them in lists.

for key,value in dic_wec_devices.items():
    print(f'##### Start of the data collection for {key} #####\n')
    my_device = value
    #if key == 'Point_Absorber_Two_Body_Model_Size_2':
    #    print('********** The value for this key is: **********')
    #    print(my_device)
    #    print('and its length is:')
    #    print(len(my_device))

    
    # defining empty list to add the wave height (Hs) and wave period (Tp) data 
    # for each combination of values
    Tp_values = []
    Hs_values = []
    Te_values = []
    Pw_values = []

    for iteration in range(len(my_device)):
        
        try:
            # getting the info about the wec type and scale
            wec_type = my_device[iteration]['wec_type']
            wec_scale = my_device[iteration]['wec_scale']
            # getting the wave height, wave period, and power data
            Tp_value = my_device[iteration]['peak_period']['value']
            Te_value = my_device[iteration]['energy_period']['value']
            Hs_value = my_device[iteration]['wave_height']['value']

            if wec_type == 'Reference Model 3':
                # Average absolute value of the PTO power(W) in heave
                #print('**************This is a Point Absorber Two Body device**************')
                Pw_value = my_device[iteration]['power_take_off_internal_heave_power']['average']['value']
            else:
                Pw_value = my_device[iteration]['power']['average']['value']

            #print(f'Iteration {iteration}:, WEC type = {wec_type}, Tp = {Tp_value}, Te = {Te_value}, Hs = {Hs_value}, Power = {Pw_value}\n{25*"-"}')    
            Tp_values.append(Tp_value)
            Te_values.append(Te_value)
            Hs_values.append(Hs_value)
            Pw_values.append(Pw_value)
        except:
            None
    
    if plot_power == True:
        # THIS WORKS BUT DOES NOT LOOK THAT GOOD
        # let's plot the three lists, Hs, Tp, and Pw such that each point is colored by the value of Pw
        #plt.figure(figsize=(10,10))
        #fig = plt.scatter(Tp_values, Hs_values, c=Pw_values, cmap='jet')
        #plt.xlabel('Tp [s]')
        #plt.ylabel('Hs [m]')
        #plt.title(f'{wec_type} - {wec_scale}')
        #plt.grid()
        ## let's add a colorbar
        #clb = plt.colorbar(fig)
        #clb.ax.set_title('Power [w]')

        # HERE TRYING BETTER WAYS PLOT
        data = {
            'wave_period': Te_values,
            'wave_height': Hs_values,
            'power_output':Pw_values
        }

        df = pd.DataFrame(data)
        #print(df.head())
        #print(df['wave_period'].min(), df['wave_period'].max())
        #print(df['wave_height'].min(), df['wave_height'].max())

        # Use pivot_table with aggregation (mean) to handle duplicate entries
        pivot_table = pd.pivot_table(df, values='power_output', index='wave_height', columns='wave_period')

        # Convert pivot table to numpy arrays
        X, Y = np.meshgrid(pivot_table.columns, pivot_table.index)
        Z = pivot_table.values

        # Create a contour plot using Matplotlib
        plt.figure(figsize=(8, 8))
        # increase the font size 
        plt.rcParams.update({'font.size': 14})

        contour = plt.contourf(X, Y, Z, cmap='YlOrRd', levels=200)  # Specify the number of contour levels
        plt.colorbar(contour, label="Power Output [W]")
        plt.title("Power Output for {} [scale={}]".format(wec_type, wec_scale), fontdict = {'fontsize' : 10})
        plt.xlabel("Wave Period [s]")
        plt.ylabel("Wave Height [m]")

        # let's save the figure as a png file
        plt.savefig(f'{wec_type}_{wec_scale}.png', bbox_inches='tight')
        # let's close the figure
        plt.close()

    # let's put these lists into a dataframe and save it as a csv file
    df = pd.DataFrame({'Tp':Tp_values, 'Te':Te_values, 'Hs':Hs_values, 'Pw':Pw_values})
    df.to_csv(f'{wec_type}_{wec_scale}.csv')
    
    #print('##################### End of the data collection for this device #####################\n')
