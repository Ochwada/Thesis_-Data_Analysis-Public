# -*- coding: utf-8 -*-
#import pandas
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
#import pandas as pd
#from pylab import rcParams
#import project_config as conf
import wind_data as wd
from helper import weib
import project_config as conf

SMOOTHNESS = 15   
#-------------------Subplot, analysis and Comparison windspeed------------------

def sub_plot_windspeed(list_of_locations, altitude_index ):

    num_locations = len(list_of_locations)
    f, list_of_plots = plt.subplots(num_locations+1, 1, sharey=True, sharex=True)

   # x = np.linspace(0, list_of_locations[0].days, list_of_locations[0].days)
    x = list_of_locations[0].get_list_of_dates_numpy()

    colors = ['r', 'g', 'b', 'm', 'c' ]
    for i in range(0,num_locations):
        w = list_of_locations[i]
        wind_x = w.windspeed[:, altitude_index]
        mean_x = wind_x.mean()
        p = list_of_plots[i]
        p.axhline(mean_x, color='grey', linewidth=0.75)
        #print('mean:' , mean_x)

        p.plot(x, w.windspeed[:,altitude_index], label=w.name, color=colors[i % len(colors)], linewidth=1.0)
        p.set_ylabel('Windspeed in [m/s]')
        p.set_title(w.name)
        p.legend()
        p.yaxis.grid(True, linestyle='dashed', linewidth=0.5)

#--------------------------Smoothing aspect-------------------------------------
    p_smoothed = list_of_plots[-1]
    for i in range(0,num_locations):
        w = list_of_locations[i]
        p_smoothed.plot(x, w.smoothed_speed(altitude_index,SMOOTHNESS),label=w.name, color=colors[i % len(colors)], linewidth=1.0)
    p_smoothed.set_title('Moving averages : n = ' + str(SMOOTHNESS) + ' days ')
    p_smoothed.set_ylabel('Windspeed in [m/s]')
    p.legend()
    plt.show()
    
#-------------------Subplot, analysis and Comparison wind power-----------------

def sub_plot_windpower( list_of_locations, altitude_index ):

    num_locations = len(list_of_locations)
    f, list_of_plots = plt.subplots(num_locations+1, 1, sharey=True, sharex=True)

   # x = np.linspace(0, list_of_locations[0].days, list_of_locations[0].days)
    x = list_of_locations[0].get_list_of_dates_numpy()

    colors = ['r', 'g', 'b', 'm', 'c' ]
    for i in range(0,num_locations):
        w = list_of_locations[i]
        wind_x = w.windpower[:, altitude_index]
        mean_x = wind_x.mean()
        p = list_of_plots[i]
        p.axhline(mean_x, color='grey', linewidth=0.75)
        #print('mean:' , mean_x)

        p.plot(x, w.windpower[:,altitude_index], label=w.name, color=colors[i % len(colors)], linewidth=1.0)
        p.set_ylabel('Wind Power in $W/m^2$')
        p.set_title(w.name)
        #p.legend()
        p.yaxis.grid(True, linestyle='dashed', linewidth=0.5)

#--------------------------Smoothing aspect-------------------------------------
    p_smoothed = list_of_plots[-1]
    for i in range(0,num_locations):
        w = list_of_locations[i]
        p_smoothed.plot(x, w.smoothed_power(altitude_index,SMOOTHNESS),label=w.name, color=colors[i % len(colors)], linewidth=1.0)
    p_smoothed.set_title('Moving averages : n = ' + str(SMOOTHNESS) + ' days ')
    p_smoothed.set_ylabel('Wind Power in $W/m^2$')
    #p.legend()
    plt.show()
#==================================================================================================
def timeseriesWS(list_of_locations, list_of_alt, startdoy=0,enddoy=300):
    num_locations = len(list_of_locations)
    num_altitudes = len(list_of_alt)
    num_days = enddoy-startdoy
    x = np.linspace(0, num_days, num=num_days)
    fig, ax = plt.subplots(2,sharex=True )
    colors = ['c', 'k','r', 'b', 'm','g' ]
    for i in range(0,num_locations):
        for a in range(0,num_altitudes):

            w = list_of_locations[i]
            ws = w.get_speed(list_of_alt[a], startdoy, enddoy)
            #ax[0].plot(x, ws, label=str(conf.altitude_map[list_of_alt[a]]), color=colors[i+a % len(colors)], linewidth=1.0)     
            ax[0].plot(x, ws, label=str(w.year), color=colors[i+a % len(colors)], linewidth=1.0)     
            ax[0].set_title('Krummhorn Wind Speed data')
            ax[0].set_xlabel('Time (Days of the year)')
            ax[0].set_ylabel('Windspeed in [m/s]')
            ax[0].legend()
            ax[0].grid(True)

    for i in range(0,num_locations):
        for a in range(0,num_altitudes):
    
            w = list_of_locations[i]
            wss = w.smoothed_speed(list_of_alt[a], SMOOTHNESS,startdoy, enddoy)
            ax[1].plot(x, wss,label=w.name, color=colors[i+a  % len(colors)], linewidth=1.0)
    ax[1].set_title('Moving averages : n = ' + str(SMOOTHNESS) + ' days ')
    ax[1].set_ylabel('Windspeed in [m/s]')
    ax[1].grid(True)
    plt.show()   

#==================================================================================================
def timeseriesWPD(list_of_locations, list_of_alt, startdoy=0,enddoy=365):
    num_locations = len(list_of_locations)
    num_altitudes = len(list_of_alt)
    num_days = enddoy-startdoy
    x = np.linspace(0, num_days, num=num_days)
    fig, ax = plt.subplots(2,sharex=True )
    colors = ['c', 'k','r', 'b', 'm','g' ]
    for i in range(0,num_locations):
        for a in range(0,num_altitudes):

            w = list_of_locations[i]
            ws = w.get_power(list_of_alt[a], startdoy, enddoy)
            ax[0].plot(x, ws, label=str(conf.altitude_map[list_of_alt[a]]) + ' m ', color=colors[i+a % len(colors)], linewidth=1.0)     
            #ax[0].plot(x, ws, label=str(w.year), color=colors[i+a % len(colors)], linewidth=1.0)     
            ax[0].set_title('Krummhorn Potential Wind Power Production')
            ax[0].set_ylabel('Wind Power in $W/m^2$')
            #--
            ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, shadow=True)
            #ax[0].legend()
            ax[0].grid(True)

    for i in range(0,num_locations):
        for a in range(0,num_altitudes):
    
            w = list_of_locations[i]
            wss = w.smoothed_power(list_of_alt[a], SMOOTHNESS,startdoy, enddoy)
            ax[1].plot(x, wss,label=w.name, color=colors[i+a  % len(colors)], linewidth=1.0)
    ax[1].set_title('Moving averages : n = ' + str(SMOOTHNESS) + ' days ')
    ax[1].set_ylabel('Wind Power in $W/m^2$')
    ax[1].set_xlabel('Time (Days of the year)')
    ax[1].grid(True)
    plt.show()   

#================================================================================================== 
# -----------------------------------------------------------------------
#correlogramWSP
# -----------------------------------------------------------------------  

        
#================================================================================================== 

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':

    print("plotwinddata.py")
    print("Loading WindMeasurements...")
    
#-----------------------------------------------------------     
#--correlogram and auto correlation   - Compute for 0-9    
    #powerall = conf.load_all_windpower()
    
    Krummhorn = wd.WindMeasurements().load(wd.WindMeasurements.createfilename(2008,53.5,8.5))
    #correlogramWSP([Krummhorn],9)
#-------------------------------------------------------------------------------
#--Horizontal Profile
    indata_Krummhorn = wd.WindMeasurements().load(wd.WindMeasurements.createfilename(2008,53.5,8.5))
    indata_Halle = wd.WindMeasurements().load(wd.WindMeasurements.createfilename(2008,51.5, 12.0)) 
    indata_Konigssee = wd.WindMeasurements().load(wd.WindMeasurements.createfilename(2008,47.5,13.5))   
#-------
#-- Multi Plot of Windspeeds
    #sub_plot_windspeed([indata_Krummhorn, indata_Halle, indata_Konigssee], 1) 
#-- Multi Plot of Windpower
    #sub_plot_windpower([indata_Krummhorn, indata_Halle, indata_Konigssee], 1) 

#===================================================================================================
#--Verticle Profile
   
#===================================================================================================
#--Year Profile
    Krumm7 = wd.WindMeasurements().load(wd.WindMeasurements.createfilename(2007,53.5,8.5))
    Krumm8 = wd.WindMeasurements().load(wd.WindMeasurements.createfilename(2008,53.5,8.5))   
    Krumm9 = wd.WindMeasurements().load(wd.WindMeasurements.createfilename(2009,53.5,8.5))
    #timeseriesWS([Krumm7], [1,3,5,7,9])
    #timeseriesWS([Krumm7,Krumm9 ], [1])
    #timeseriesWPD([Krumm7,Krumm8,Krumm9 ], [1])
    timeseriesWPD([Krumm7], [1,3,5,7,9])
   
#====================================================================================================
   
#====================================================================================================
#--Mean Value
    Krumm_data = wd.WindMeasurements().load(wd.WindMeasurements.createfilename(2007,53.5,8.5))
    Krumm = Krumm_data.windpower[:,1]
    Krumm_mean= np.mean(Krumm )
   # print(Krumm_mean)
#================================================================================
