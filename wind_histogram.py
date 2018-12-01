# -*- coding: utf-8 -*-
# -*- codiing for wind_histogram -*-

import matplotlib.pyplot as plt
import numpy as np
#import scipy.stats as stats
from scipy import stats
import matplotlib.mlab as mlab
import statsmodels.api as sm
import wind_data as wd
import plot_winddata as pwd
from helper import date_to_doy, doy_to_date, moving_average, altitude_to_int, weib
import project_config as conf
import math
#import matplotlib.font_manager as font_manager

axis_font = {'fontname':'Arial', 'size':'16'}

# -----------------------------------------------------------------------
#Central Tendency
# -----------------------------------------------------------------------
#mean
def mean_speed(data): 
    total = 0
    mean = 0
    for item in data:
        total += item
    mean_speed = total/float(len(data))
    return mean_speed
    
def mean_power(data): 
    total = 0
    mean = 0
    for item in data:
        total+= item
    mean_power = total/float(len(data))
    return mean_power
# -----------------------------------------------------------------------
#Weibull pdf
# -----------------------------------------------------------------------

def weibull_plot_speed(data, params):
    bins = np.arange(0, 32.0, 0.5)
    plt.hist(data, bins, histtype='bar', edgecolor='black',normed=True, alpha=0.5, rwidth=1.0);
    x = np.arange(0, 32.0, 0.1)
    plt.plot(x,stats.exponweib.pdf(x, *params), label="Weibull PDF")
    mean_value = data.mean()
    plt.axvline(mean_value, color='m', linestyle='dashed', linewidth=1, label="Mean power" )
    #plt.title('Wind speed distribution for Germany at Level 1')
    plt.xlabel('Wind Speed (m/s)', **axis_font)
    plt.ylabel('Wind speed frequency', **axis_font)
    plt.legend(loc=1, prop={'size': 16})
    plt.show()
    #plt.savefig('image1')


    
    #print(result)
#=======================================================================
if __name__ == '__main__':
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

#Central Tendancy   - Compute for 0-9
    speedall = conf.load_all_windspeeds()
    meanspeed = mean_speed(speedall[:,1])
    #print(meanspeed)
    
    powerall = conf.load_all_windpower()
    meanpower = mean_power(powerall[:,8])
    #print(meanpower)
    
#--------------------------Weibull PDF---------------------- 
#----------------------------------------------------------- 

#------------windspeed
    speedall = conf.load_all_windspeeds()
    data_speed = speedall [:,1]
    #params_speed = stats.exponweib.fit(data_speed,floc=0)
    
    #windspeed -----stats.exponweib.fit(data_speed,floc=0)
    params_speed =  (1.1113449643109912, 1.6809413157101651, 0, 7.2972382976005772)#Level 1
    #params_speed =(1.0635878486058918, 1.7129895275983615, 0, 8.0111689684382323)#Level 2
    #params_speed =(1.0704643275819068, 1.6853620845145747, 0, 8.3604171276602486)#Level 3
    #params_speed =(1.1113173256840196, 1.6301269094327573, 0, 8.4365496561132183)#Level 4
    #params_speed =(1.1600496620157552, 1.5765771265205082, 0, 8.4068808687607639)#Level 5
    #params_speed =(1.2147903730266001, 1.5256215491691232, 0, 8.3224080743411264)#Level 6
    #params_speed =(1.2558199288860206, 1.4950921999766487, 0, 8.2474385764630327)#Level 7
    #params_speed =(1.2949475501898591, 1.469286787656831, 0, 8.1859121591777537)#Level 8
    #params_speed =(1.3035611603623392, 1.4695586916574541, 0, 8.2236837246717638)#Level 9

    print('p\n', params_speed)
    #weibull_plot_speed(data_speed, params_speed)

#------------windpower
    dist = stats.lognorm
    powerall = conf.load_all_windpower()
    data_power = powerall [:,9]
    #params_power = dist.fit(data_power,floc=0)
    
    params_power = (2.1848911866776488, 0, 195.85401224562315) #lognorm
    print('p\n', params_power)

    #--2--params_power=(1.0945801093499283, 0.56150661053208051, 0, 274.89152413198588)#Level 1
    #weibull_plot_power(data_power, params_power, dist)
    
#==================================================================================================     
#------------windpower location base  --------
    dist = stats.lognorm 
    wind_Konigssee = wd.WindMeasurements().load(conf.connected_filename(47.5, 13.5) )
    data_power_Konigssee = wind_Konigssee.windpower[:,9]
    params_power_Konigssee = dist.fit(data_power_Konigssee,floc=0)
    print('p\n', params_power_Konigssee)
    #weibull_plot_power(data_power_Konigssee, params_power_Konigssee, dist)
    
    
#------------------------------------------------- 
#------------------------------------------------- 
   
    #speedall = conf.load_all_windspeeds()
    #mediumspeed = median_speed(speedall [:,0])
    #print(mediumspeed)

    #powerall = conf.load_all_windpower()
    #mediumpower = median_power(powerall [:,0])
    #print(mediumpower)
   

# -----------------------------------------------------------------------
    
     #indata_Konigssee = wd.WindMeasurements().load(conf.connected_filename(47.5, 13.5) ) # Ten years at this location
     #check_distribution(indata_Konigssee.get_windspeed_at(0))

     #speedall = conf.load_all_windspeeds() # np.load(conf.npz_folder_path + "windspeed_complete.npz", allow_pickle=False)['arr_0']
     #powerall = conf.load_all_windpower() # np.load(conf.npz_folder_path + "windspower_complete.npz", allow_pickle=False)['arr_0']


     #print(speedall.shape)
     #check_distribution(speedall[:,1])
    #pass