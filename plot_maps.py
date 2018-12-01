# -*- coding: utf-8 -*-
# -*- coding for ------plot_map-------  -*-

import project_config as conf
import wind_data as wd
import helper as hp
import numpy as np
import mpl_toolkits.basemap as bm
from mpl_toolkits.basemap import cm, Basemap, shiftgrid
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon 
from matplotlib.collections import PatchCollection 
import matplotlib.patches as patches

#--------------------------------
#from matplotlib.collections import LineCollection 
#from matplotlib.patches import PathPatch 
#from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
#from mpl_toolkits.axes_grid1.inset_locator import mark_inset
#import numpy.ma as ma
#from matplotlib import colors as c
#import mpl_toolkits as mpl
#import cartopy.crs as ccrs
#import cartopy.feature as cft
#from cmocean import cm as cmo
    
def simpleplot( data, year_str, alt):
    fig = plt.figure()
    fig.subplots_adjust(right=0.8)
   
    vmin = data.min()
    vmax = data.max()
    #print( vmin, vmax)
    
    gridlats, gridlongs = hp.get_grid()
    [lonall, latall] = np.meshgrid(gridlongs,gridlats)
    mapproj = bm.Basemap(projection='stere', lon_0=np.mean(gridlongs),lat_0=np.mean(gridlats),lat_ts=10.0, \
                       llcrnrlat=47.0, llcrnrlon=5.0, \
                        urcrnrlat=55.5, urcrnrlon=16.0, \
                        rsphere=6371200.,resolution='l',area_thresh=10000)
    mapproj.drawcoastlines()
    mapproj.drawcountries()
    mapproj.shadedrelief()
    #--------------------------------
    hfont = {'fontname':'Georgia', 'fontsize': 22}
    
    Berlin_x, Berlin_y = mapproj(13.404, 52.520)
    plt.plot(Berlin_x, Berlin_y, 'ok', markersize=3)
    plt.text(Berlin_x, Berlin_y, 'Berlin', fontsize=8, **hfont, ha='right')
    
    Munich_x, Munich_y = mapproj(11.576, 48.137)
    plt.plot(Munich_x, Munich_y, 'ok', markersize=3)
    plt.text(Munich_x, Munich_y, 'Münich', fontsize=8, **hfont, ha='right')
    
    Stuttgart_x, Stuttgart_y = mapproj(9.177, 48.782)
    plt.plot(Stuttgart_x, Stuttgart_y, 'ok', markersize=3)
    plt.text(Stuttgart_x, Stuttgart_y, 'Stuttgart', fontsize=8, **hfont, ha='right')
    
    Freiburg_x, Freiburg_y = mapproj(7.8527, 47.995)
    plt.plot(Freiburg_x, Freiburg_y, 'ok', markersize=3)
    plt.text(Freiburg_x,Freiburg_y, 'Freiburg', fontsize=8, **hfont,ha='right')
    
    Krum_x, Krum_y = mapproj(7.016, 53.404)
    plt.plot(Krum_x, Krum_y, 'ok', markersize=3)
    plt.text(Krum_x, Krum_y, ' Krummhörn', fontsize=8, **hfont, ha='right')
    
    Halle_x, Halle_y = mapproj(11.968, 51.497)
    plt.plot(Halle_x, Halle_y, 'ok', markersize=3)
    plt.text(Halle_x, Halle_y, 'Halle', fontsize=8, **hfont, ha='right')
    
    Sch_x, Sch_y = mapproj(12.989, 47.602)
    plt.plot(Sch_x, Sch_y, 'ok', markersize=3)
    plt.text(Sch_x, Sch_y, 'Schönau am Königssee', fontsize=8, **hfont,ha='right')
    #--------------------------------
    ny = data.shape[0]; nx = data.shape[1]
    lons, lats = mapproj.makegrid(nx, ny)
    x ,y = mapproj(lons, lats)
    
   # mymap = mapproj.contourf(x,y,data[:,:,alt],20, origin='lower', cmap=plt.cm.jet,clim=(vmin, vmax),alpha=1.0)
    clim = np.linspace(0,1700,35, endpoint=True)
    mymap = mapproj.contourf(x,y,data[:,:,alt], clim, cmap=plt.cm.jet,alpha=1.0)

    cbar = mapproj.colorbar(mymap)
    #--------------------------------------
    cbar.set_label('Mean $P_{wpd}$ in $W/m^2$ ')
    plt.title('Mean $P_{wpd}$ for ' + year_str+ ' at Level '+ str(alt))
    #---------------------------------
    #plt.title('Mean Wind Power Density for ' + str(year)+ ' at Level '+ str(alt))

    #plt.title('Relief')
    
    #--------------------------------

    plt.show()
    #------Important--------------------------
    #plt.savefig(conf.image_path+"map"+year_str+"_"+str(alt)+".png")
    #plt.savefig(conf.eps_path+"map"+year_str+"_"+str(alt)+".eps")
    #print( "save: ", conf.eps_path+"map"+year_str+"_"+str(alt))
    
def simpleplot2( data, year_str, alt):
    fig = plt.figure()
    fig.subplots_adjust(right=0.8)
   
    vmin = data.min()
    vmax = data.max()
    #print( vmin, vmax)   
    
    gridlats, gridlongs = hp.get_grid()
    [lonall, latall] = np.meshgrid(gridlongs,gridlats)
    mapproj = bm.Basemap(projection='stere', lon_0=np.mean(gridlongs),lat_0=np.mean(gridlats),lat_ts=10.0, \
                       llcrnrlat=47.0, llcrnrlon=5.0, \
                        urcrnrlat=55.5, urcrnrlon=16.0, \
                        rsphere=6371200.,resolution='l',area_thresh=10000)
    mapproj.drawcoastlines()
    mapproj.drawcountries()
    mapproj.shadedrelief()
    
    #--------------------------------
    hfont = {'fontname':'Georgia'}
    
    Berlin_x, Berlin_y = mapproj(13.404, 52.520)
    plt.plot(Berlin_x, Berlin_y, 'ok', markersize=3)
    plt.text(Berlin_x, Berlin_y, 'Berlin', fontsize=8, **hfont, ha='right')
    
    Munich_x, Munich_y = mapproj(11.576, 48.137)
    plt.plot(Munich_x, Munich_y, 'ok', markersize=3)
    plt.text(Munich_x, Munich_y, 'Münich', fontsize=8, **hfont, ha='right')
    
    Stuttgart_x, Stuttgart_y = mapproj(9.177, 48.782)
    plt.plot(Stuttgart_x, Stuttgart_y, 'ok', markersize=3)
    plt.text(Stuttgart_x, Stuttgart_y, 'Stuttgart', fontsize=8, **hfont, ha='right')
    
    Freiburg_x, Freiburg_y = mapproj(7.8527, 47.995)
    plt.plot(Freiburg_x, Freiburg_y, 'ok', markersize=3)
    plt.text(Freiburg_x,Freiburg_y, 'Freiburg', fontsize=8, **hfont,ha='right')
    
    Krum_x, Krum_y = mapproj(7.016, 53.404)
    plt.plot(Krum_x, Krum_y, 'ok', markersize=3)
    plt.text(Krum_x, Krum_y, ' Krummhörn', fontsize=8, **hfont, ha='right')
    
    Halle_x, Halle_y = mapproj(11.968, 51.497)
    plt.plot(Halle_x, Halle_y, 'ok', markersize=3)
    plt.text(Halle_x, Halle_y, 'Halle', fontsize=8, **hfont, ha='right')
    
    Sch_x, Sch_y = mapproj(12.989, 47.602)
    plt.plot(Sch_x, Sch_y, 'ok', markersize=3)
    plt.text(Sch_x, Sch_y, 'Schönau am Königssee', fontsize=8, **hfont,ha='right')
    #--------------------------------
    ny = data.shape[0]; nx = data.shape[1]
    lons, lats = mapproj.makegrid(nx, ny)
    x ,y = mapproj(lons, lats)
    
   # mymap = mapproj.contourf(x,y,data[:,:,alt],20, origin='lower', cmap=plt.cm.jet,clim=(vmin, vmax),alpha=1.0)
    clim = np.linspace(0,12,25, endpoint=True)
    mymap = mapproj.contourf(x,y,data[:,:,alt], clim, cmap=plt.cm.jet,alpha=1.0)

    cbar = mapproj.colorbar(mymap)
    #--------------------------------------

    cbar.set_label('Mean $W_s$ in $m/s$ ')
    plt.title('Mean $W_s$ for ' + year_str+ ' at Level '+ str(alt))
    
    #---------------------------------
    #plt.title('Mean Wind Power Density for ' + str(year)+ ' at Level '+ str(alt))

    #plt.title('Relief')
    
    #--------------------------------

    plt.show()


def simpleplot3( data, year_str, alt):
    fig = plt.figure()
    fig.subplots_adjust(right=0.8)
   
    vmin = data.min()
    vmax = data.max()
    #print( vmin, vmax)
    
    
    gridlats, gridlongs = hp.get_grid()
    [lonall, latall] = np.meshgrid(gridlongs,gridlats)
    mapproj = bm.Basemap(projection='stere', lon_0=np.mean(gridlongs),lat_0=np.mean(gridlats),lat_ts=10.0, \
                       llcrnrlat=47.0, llcrnrlon=5.0, \
                        urcrnrlat=55.5, urcrnrlon=16.0, \
                        rsphere=6371200.,resolution='l',area_thresh=10000)
    mapproj.drawcoastlines()
    mapproj.drawcountries()
    mapproj.shadedrelief()
    
    #--------------------------------
    hfont = {'fontname':'Georgia'}
    
    Berlin_x, Berlin_y = mapproj(13.404, 52.520)
    plt.plot(Berlin_x, Berlin_y, 'ok', markersize=3)
    plt.text(Berlin_x, Berlin_y, 'Berlin', fontsize=8, **hfont, ha='right')
    
    Munich_x, Munich_y = mapproj(11.576, 48.137)
    plt.plot(Munich_x, Munich_y, 'ok', markersize=3)
    plt.text(Munich_x, Munich_y, 'Münich', fontsize=8, **hfont, ha='right')
    
    Stuttgart_x, Stuttgart_y = mapproj(9.177, 48.782)
    plt.plot(Stuttgart_x, Stuttgart_y, 'ok', markersize=3)
    plt.text(Stuttgart_x, Stuttgart_y, 'Stuttgart', fontsize=8, **hfont, ha='right')
    
    Freiburg_x, Freiburg_y = mapproj(7.8527, 47.995)
    plt.plot(Freiburg_x, Freiburg_y, 'ok', markersize=3)
    plt.text(Freiburg_x,Freiburg_y, 'Freiburg', fontsize=8, **hfont,ha='right')
    
    Krum_x, Krum_y = mapproj(7.016, 53.404)
    plt.plot(Krum_x, Krum_y, 'ok', markersize=3)
    plt.text(Krum_x, Krum_y, ' Krummhörn', fontsize=8, **hfont, ha='right')
    
    Halle_x, Halle_y = mapproj(11.968, 51.497)
    plt.plot(Halle_x, Halle_y, 'ok', markersize=3)
    plt.text(Halle_x, Halle_y, 'Halle', fontsize=8, **hfont, ha='right')
    
    Sch_x, Sch_y = mapproj(12.989, 47.602)
    plt.plot(Sch_x, Sch_y, 'ok', markersize=3)
    plt.text(Sch_x, Sch_y, 'Schönau am Königssee', fontsize=8, **hfont,ha='right')
    #--------------------------------
    ny = data.shape[0]; nx = data.shape[1]
    lons, lats = mapproj.makegrid(nx, ny)
    x ,y = mapproj(lons, lats)
    
    #mymap = mapproj.contourf(x,y,data[:,:,alt],20, origin='lower', cmap=plt.cm.jet,clim=(vmin, vmax),alpha=1.0)
    clim = np.linspace(0,2200,45,endpoint=True)
    mymap = mapproj.contourf(x,y,data[:,:,alt], clim, cmap=plt.cm.jet,alpha=1.0)

    cbar = mapproj.colorbar(mymap)
    #--------------------------------------

    cbar.set_label('Standard Deviation ($ \sigma$) ')
    plt.title(' $P_{wpd}$  Standard Deviation for ' + year_str+ ' at Level '+ str(alt))
    
    #---------------------------------
    #plt.title('Mean Wind Power Density for ' + str(year)+ ' at Level '+ str(alt))

    #plt.title('Relief')
    
    #--------------------------------

    plt.show()

def simpleplot4(data, year_str, alt):
    fig = plt.figure()
    ax=fig.add_subplot(1,1,1)
   
    vmin = data.min()
    vmax = data.max()
    #print( vmin, vmax)
    
    
    gridlats, gridlongs = hp.get_grid()
      
    [lonall, latall] = np.meshgrid(gridlongs,gridlats)
    
    mapproj = bm.Basemap(projection='stere', lon_0=np.mean(gridlongs),lat_0=np.mean(gridlats),lat_ts=10.0, \
                       llcrnrlat=51.9, llcrnrlon=11.9, \
                        urcrnrlat=54.1, urcrnrlon=14.1, \
                        rsphere=6371200.,resolution='l',area_thresh=10000)
    clim = np.linspace(0,1700,35, endpoint=True)                    
    mapproj.drawcoastlines()
    mapproj.drawcountries()
    mapproj.shadedrelief()
    mapproj.drawparallels(np.arange(-6.,90.,2.0),labels=[1,0,0,0])
    mapproj.drawmeridians(np.arange(-180.,360.,2.0),labels=[0,0,0,1])
    
    cmap=plt.cm.jet
   #-------------------------------- 
    airports = 'LandCover/airport'
    #rails = 'LandCover/buffer_rail'
    #roads = 'LandCover/buffer_road'
    #rails = 'Germany/New_files/Rails_buffer'
    #roads = 'Germany/New_files/Roads_buffer'
    urbans = 'LandCover/buffer_urban'
    
    mapproj.readshapefile( urbans, 'urban')
    mapproj.readshapefile( airports, 'airport' )
    mapproj.readshapefile( rails, 'rail')
    mapproj.readshapefile( roads, 'road' )
   
    infrastructure_alpha = 0.1
    
    patches_0 = []
    for info, shape in zip( mapproj.airport_info, mapproj.airport):
        if info['code_12'] == '124':
            patches_0.append(Polygon(np.array(shape), True))
    p_0= PatchCollection(patches_0, facecolor= 'white', edgecolor=None, zorder=2, alpha =0.7 )
    ax.add_collection(p_0)
    
    
    patches_1 = []
    for info, shape in zip( mapproj.rail_info, mapproj.rail):
        if info['EXS_DESCRI'] == 'Operational':
            patches_1.append(Polygon(np.array(shape), True))
    p_1= PatchCollection(patches_1, facecolor= 'brown', edgecolor=None, zorder=2, alpha =infrastructure_alpha)
    ax.add_collection(p_1)
    
    patches_2 = []
    for info, shape in zip( mapproj.road_info, mapproj.road):
        if info['F_CODE_DES'] == 'Road':
            patches_2.append(Polygon(np.array(shape), True))
    p_2= PatchCollection(patches_2, facecolor= 'dimgrey', edgecolor=None, zorder=2, alpha =infrastructure_alpha)
    ax.add_collection(p_2)
    
            
    patches_3 = []
    for info, shape in zip( mapproj.urban_info, mapproj.urban):
        if info['code_12'] == '112':
            patches_3.append(Polygon(np.array(shape), True))
    p_3= PatchCollection(patches_3, facecolor= 'wheat', edgecolor=None, zorder=2, alpha =infrastructure_alpha)
    ax.add_collection(p_3)
    #--------------------------------
    hfont = {'fontname':'Georgia'}
    
    Berlin_x, Berlin_y = mapproj(13.404, 52.520)
    plt.plot(Berlin_x, Berlin_y, 'ok', markersize=3,color='black' )
    plt.text(Berlin_x, Berlin_y, 'Berlin', fontsize=10, color='black', **hfont, ha='right')
    
    #--------------------------------
    d = hp.get_roi(data, 52.0, 54.0, 12.0, 14.0) 

    ny =d.shape[0]; nx = d.shape[1]
    lons, lats = mapproj.makegrid(nx, ny)
    x ,y = mapproj(lons, lats)
    #--------------------------------
    #mymap = mapproj.contourf(x,y,data[:,:,alt],clim , cmap=cmap, shading='interp',alpha=1.0)
    mymap = mapproj.contourf(x,y,d[:,:,alt],clim , cmap=cmap, shading='interp',alpha=1.0)
    cbar = mapproj.colorbar(mymap)
    #--------------------------------------
    cbar.set_label('Mean $P_{wpd}$ in $W/m^2$ ')
    
    plt.title('Mean $P_{wpd}$ at Level '+ str(alt))
    #-------------------------------

    plt.show()
    
#===================
ALL_YEARS = True
#ALL_YEARS = False


#year = 2007
#alt = 3
if __name__ == '__main__':
    
#==================================================================================================
    maps = hp.load_maps( all_years=ALL_YEARS)
    mean_windpower = maps['windpower_mean_map']
    simpleplot4(mean_windpower, year_str="2007 to 2016", alt=1)
    
    
    #===================================================================
#--Try
    maps = hp.load_maps( all_years=ALL_YEARS)
    mean_windpower = maps['windpower_mean_map']
    #print(mean_windpower)
    
#==================================================================================================
    if  ALL_YEARS:
        maps = hp.load_maps( all_years=ALL_YEARS)
        # print(maps.keys())
        for alt in conf.altitude_indices:

            mean_windspeeds = maps['windspeed_mean_map']
            mean_windpower = maps['windpower_mean_map']
            stddev_windpower = maps['windpower_stddev_map']
            
            #simpleplot(mean_windpower, year_str="2007 to 2016", alt=alt)
            #simpleplot2(mean_windspeeds, year_str="2007 to 2016", alt=alt)
            #simpleplot3(stddev_windpower, year_str="2007 to 2016", alt=alt)
            simpleplot4(mean_windpower, year_str="2007 to 2016", alt=alt)

    else:
        for year in conf.years:

            maps= hp.load_maps(year, all_years=ALL_YEARS)
            #print(maps.keys())

            for alt in conf.altitude_indices:

                mean_windspeeds = maps['windspeed_mean_map']
                mean_windpower = maps['windpower_mean_map']
                stddev_windpower = maps['windpower_stddev_map']




                simpleplot(mean_windpower, year_str=str(year), alt=alt)
                #simpleplot(stddev_windpower,3)

                #plt.waitforbuttonpress()


    exit(0)
