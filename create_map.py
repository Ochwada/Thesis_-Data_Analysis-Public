import project_config as conf
import wind_data as wd
import helper as hp
import numpy as np
import datetime as dt

#
year = 2016
#year = 2015
#print for all years

##whole year average
start_day_of_year = 0
end_day_of_year = -1
compress = False

#ALL_YEARS = False
ALL_YEARS = True

##example for averageing over first quater
#start_day_of_year = hp.date_to_doy(dt.date(year, 1, 1))
#end_day_of_year = hp.date_to_doy(dt.date(year, 4, 1))


if __name__ == '__main__':


    ## create numpyarrays  to hold hold data  ( one for each map  (so each altitude you want to use)
    ##do it for all maps you want to create. so you don't have to iterate over all positions multiple times
    windpower_mean_map = np.ndarray((conf.num_locations_lat, conf.num_locations_long, conf.num_locations_alt), np.float64)
    windspeed_mean_map = np.ndarray((conf.num_locations_lat, conf.num_locations_long, conf.num_locations_alt), np.float64)

    windpower_stddev_map = np.ndarray((conf.num_locations_lat, conf.num_locations_long, conf.num_locations_alt), np.float64)
    #map_array_windspeed_mean = np.ndarray((conf.num_locations_lat, conf.num_locations_long, conf.num_locations_alt),np.float64)
    #print(map_array_windpower)

    #iterate over all locations in conf.locations

    for coordinate in conf.locations:
        print(coordinate)

        lat,long = coordinate #split into single values

        if ALL_YEARS :
            wind_data = wd.WindMeasurements().load(conf.connected_filename(lat, long))
        else:
            wind_data = wd.WindMeasurements().load(wd.WindMeasurements.createfilename(year, lat, long))

        index_lat, index_long = hp.coord_to_indices(lat, long)

        #print(index_lat, index_long) #define indexing*

        windpower_mean_map[index_lat, index_long]
        windspeed_mean_map[index_lat, index_long]

        windpower_stddev_map[index_lat, index_long]

        #print(map_array_windpower[index_lat, index_long] )


        for index_alt in range(conf.num_locations_alt):
            #print(index_alt)
            mean_power = wind_data.mean_power(index_alt, start_day_of_year, end_day_of_year)
            mean_speed = wind_data.mean_speed(index_alt, start_day_of_year, end_day_of_year)
            stddev_power = wind_data.stddev_power(index_alt, start_day_of_year, end_day_of_year)

            #print("mean wind power for time range: ",  start_day_of_year, end_day_of_year)
            windpower_mean_map[index_lat, index_long, index_alt] = mean_power

            windspeed_mean_map[index_lat, index_long, index_alt] = mean_speed

            windpower_stddev_map[index_lat, index_long, index_alt] = stddev_power

            #print(tmp)

    #Call the save function

    hp.save_maps({'windspeed_mean_map':windspeed_mean_map, 'windpower_mean_map':windpower_mean_map, 'windpower_stddev_map':windpower_stddev_map},year, ALL_YEARS)
    pass

