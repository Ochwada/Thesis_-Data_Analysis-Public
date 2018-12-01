import glob

import wind_data as wd  #
import numpy as np
import project_config as conf
import re

from helper import date_to_doy, doy_to_date, moving_average, altitude_to_int

def connect_windmeasurements_for_location(latitude, longitude, list_of_years):
    first = True
    res = 0
    for y in list_of_years:
        w = wd.WindMeasurements().load(wd.WindMeasurements.createfilename(y, latitude, longitude))

        if first:
            res = w
            first = False
            # print(res)
        else:
            res.append(w)
            # print(res)

    return res


if __name__ == '__main__':

    # Reading Locations from NPZ filenames (stored in conf by hand)
    # filenames = sorted(glob.glob(conf.get_data_globstring_for_year( 2007 ), recursive=True))
    # locations = []
    # for fn in filenames:
    #     r = r'(\d+)'  # return digit -finds everything that is made out of digits (\d for digit)
    #     year, lat, long = re.findall(r, fn)
    #     locations.append( (int(lat)/10.0, int(long)/10.0) )
    #
    # print(locations)
    #np_all_speed = np.array([], dtype=np.float64)
    #np_all_power = np.array([], dtype=np.float64)
    if True:
        first = True
        for  lat, long in conf.locations:
            #print( lat, " ", long)

            w = connect_windmeasurements_for_location(lat, long, list(range(2007, 2016 + 1)))

            fname = conf.connected_filename(lat,long)
            print("save as:", fname )
            w.save(fname)

#
#             if first:
#
#                 np_all_speed = w.windspeed
#                 np_all_power = w.windpower
#                 first = False
#             else:
#                 np_all_speed = np.append(np_all_speed, w.windspeed, axis= 0)
#                 np_all_power= np.append(np_all_power, w.windpower, axis= 0)
#
#         np.savez(conf.npz_folder_path+"windspeed_complete.npz", np_all_speed)
#         np.savez(conf.npz_folder_path+"windpower_complete.npz", np_all_power)
#
#     #speedall = np.load(conf.npz_folder_path+"windspeed_complete.npz", allow_pickle=False)
#     #powerall = np.load(conf.npz_folder_path+"windpower_complete.npz", allow_pickle=False)
#
#     #speedall[:,altidute_index]
#     if False:
#         by_year_speed= {}
#         by_year_power= {}
#
#         first = True
#
#         for y in range(2007, 2016 + 1):
#             for lat, long in conf.locations:
#                 w = wd.WindMeasurements().load(wd.WindMeasurements.createfilename(y, lat, long))
#                 if not y in by_year:
#                     by_year_speed[y] = w.windspeed
#                     by_year_power[y] = w.windpower
#                     first = False
#                 else:
#                     by_year_speed[y] = np.append(by_year_speed[y], w.windspeed, axis=0)
#                     by_year_power[y] = np.append(by_year_power[y], w.windpower, axis=0)
#
#
#
#         np.savez(conf.npz_folder_path+"windspeed_years.npz", by_year_speed)
#         np.savez(conf.npz_folder_path +"windpower_years.npz", by_year_power)
#
# #"DATA/ALL/NPZ
#
#     ##loading
#         by_year =  np.load(conf.npz_folder_path+"windspeed_years.npz")
#         print (by_year.files)
#         ws2007 = by_year['2007']
