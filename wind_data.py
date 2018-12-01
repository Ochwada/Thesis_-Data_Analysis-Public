import glob, sys
#from datetime import datetime
import datetime as dt

import numpy as np
import project_config as conf
import calendar
import re

from helper import date_to_doy, doy_to_date, moving_average, altitude_to_int



class WindMeasurements():
    def __init__(self, name="", latitude=0.0, longitude=0.0, altitude=0.0, year=0.0, surface_u=0.0,
                 surface_v=0.0, surface_r=0.0, min_altitude=0.1, max_altitude=1.0,
                 altitude_step_width=0.1):

        if calendar.isleap(year):  # check for leap year
            self.days = 366
        else:
            self.days = 365

        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.year = year   ## starting year in terms of multiple yearspan
        self.surface_u = surface_u
        self.surface_v = surface_v
        self.surface_r = surface_r
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude
        self.altitude_step_width = altitude_step_width

        self.num_altitude_steps = int((max_altitude - min_altitude) / altitude_step_width) + 1
        #self.altitude_map = [int(min_altitude +((i+1)*altitude_step_width) *1000) for i in range(self.num_altitude_steps)]

        self.windspeed = np.zeros((self.days, self.num_altitude_steps), dtype=np.float64)
        self.windpower = np.zeros((self.days, self.num_altitude_steps), dtype=np.float64)

    def __str__(self):
        tmp = ""
        tmp += self.name + "\n"
        tmp += "(" + str(self.latitude)
        tmp += "," + str(self.longitude)
        tmp += "," + str(self.altitude) + ")\n"
        tmp += "year: " + str(self.year)
        tmp += "\n surface_u: " + str(self.surface_u)
        tmp += "\n surface_v: " + str(self.surface_v)
        tmp += "\n surface_r: " + str(self.surface_r)
        tmp += "\n Minimum altitude: " + str(self.min_altitude)
        tmp += "\n Maximum altitude: " + str(self.max_altitude)
        tmp += "\n Altitude range: " + str(self.altitude_step_width)
        tmp += "\n number of altitude: " + str(self.num_altitude_steps)
        tmp += "\n windspeed \n: " + str(self.windspeed)
        tmp += "\n windpower \n: " + str(self.windpower)
        tmp += "\n altitude map:\n" + str(self.altitude_map)

        return tmp

    def save(self, filename="", compress=False):
        if filename == "":
            filename = WindMeasurements.createfilename(self.year, self.latitude, self.longitude)
        save_dictionary = self.__dict__
        #print(save_dictionary)
        if 'altitude_map' in self.__dict__:
            save_dictionary['altitude_map'] = np.array(save_dictionary['altitude_map'])
        if compress:
            np.savez_compressed(filename, **save_dictionary)
        else:
            np.savez(filename, **save_dictionary)

    def load(self, filename):  # Loading and saving
        data = np.load(filename, allow_pickle=False)  # stucture similar to dic but not a dictionary
        self.days = int(data['days'])
        self.name = str(data['name'])
        self.latitude = float(data['latitude'])
        self.longitude = float(data['longitude'])
        self.altitude = float(data['altitude'])
        self.year = int(data['year'])
        self.surface_u = float(data['surface_u'])
        self.surface_u = float(data['surface_v'])
        self.surface_u = float(data['surface_r'])
        self.min_altitude = float(data['min_altitude'])
        self.max_altitude = float(data['max_altitude'])
        self.altitude_step_width = float(data['altitude_step_width'])

        self.num_altitude_steps = int(data['num_altitude_steps'])
        self.windspeed = data['windspeed']
        self.windpower = data['windpower']

        self.altitude_map = data['altitude_map'].tolist()

        return self

    def get_windspeed_at(self, altitude_index):
        return self.windspeed[:,altitude_index]

    def get_windpower_at(self, altitude_index):
        return self.windpower[:,altitude_index]

    def get_windspeed_at_day(self, doy):
        return self.windspeed[doy, :]

    def get_windspeed_at_day(self, doy):
        return self.windpower[doy, :]

    def get_power(self, altitude_index, start_doy=0, end_doy=-1):
        return self.windpower[start_doy:end_doy, altitude_index]

    def get_speed(self, altitude_index, start_doy=0, end_doy=-1):
        return self.windspeed[start_doy:end_doy, altitude_index]
##############
    def sum_power(self, altitude_index, start_doy=0, end_doy=-1):
        if end_doy == -1:
            end_doy = self.days
        return self.windpower[start_doy:end_doy, altitude_index].sum(), end_doy - start_doy

    def sum_speed(self, altitude_index, start_doy=0, end_doy=-1):
        if end_doy == -1:
            end_doy = self.days
        return self.windspeed[start_doy:end_doy, altitude_index].sum(), end_doy - start_doy
###############


    def mean_power(self, altitude_index, start_doy=0, end_doy=-1):
        if end_doy == -1:
            end_doy = self.days
        return self.windpower[start_doy:end_doy, altitude_index].mean()

    def mean_speed(self, altitude_index, start_doy=0, end_doy=-1):
        if end_doy == -1:
            end_doy = self.days
        return self.windspeed[start_doy:end_doy, altitude_index].mean()

    def stddev_power(self, altitude_index, start_doy=0, end_doy=-1):
        if end_doy == -1:
            end_doy = self.days
        return self.windpower[start_doy:end_doy, altitude_index].std()

    def stddev_speed(self, altitude_index, start_doy=0, end_doy=-1):
        if end_doy == -1:
            end_doy = self.days
        return self.windspeed[start_doy:end_doy, altitude_index].std()

    def smoothed_speed(self, altitude_index,N,start_doy=0, end_doy=-1):
        return moving_average(self.get_speed(altitude_index, start_doy, end_doy), N)

    def smoothed_power(self, altitude_index, N,start_doy=0, end_doy=-1):
        return moving_average(self.get_power(altitude_index, start_doy, end_doy), N)

    def get_list_of_dates(self):
        lst = []
        for d in range(0, self.days ):
            lst.append(doy_to_date(d, self.year))
        return lst

    def get_list_of_dates_numpy(self):
        lst = self.get_list_of_dates()
        return np.array(lst, dtype=np.datetime64)


    #def altitude_to_index(self, alt):
    #    return self.altitude_map.index(alt)

    #def index_to_altitude(self, ind):
    #    return self.altitude_map[ind];


    def append(self, wmeas):
        #TODO for all other data assert that self.* == wmeas.*
        assert self.year <= wmeas.year

        self.days += wmeas.days
        self.windspeed = np.append(wmeas.windspeed, self.windspeed, axis=0)
        self.windpower = np.append(wmeas.windpower, self.windpower, axis=0)

    @staticmethod
    def createfilename(year, latitude, longitude ):
        tmp = conf.npz_folder_path
        tmp += str(year) + "/"  # creating a string
        tmp += "winddata_" + str(int(latitude * 10)) + "_"
        tmp += str(int(longitude * 10))
        tmp += ".npz"
        return tmp

        # -------------------------------------------------------------------------------------


class WindDataConverter():
    def __init__(self, globstring, min_altitude=0.1, max_altitude=1.0,
                 altitude_step_width=0.1):
        self.windfiles = sorted(glob.glob(globstring, recursive=True))
        self.dict_winddata = {}
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude
        self.altitude_step_width = altitude_step_width
        self.num_altitude_steps = int((max_altitude - min_altitude) / altitude_step_width) + 1

        print(self.windfiles)

    def __getattr__(self, name):
        if not self.F:
            print("loading %s" % self.windfile)
        return object.__getattribute__(self.F, name)


    def parse_line(self, line, year_file, day):
        # wakati = dt.date(int(token[0]), int(token[1]), 1)
        token = line.split()
        index_string = token[2] + "x" + token[3]
        print('process line: ' , index_string, " y:", year_file, " d:", day )
        if index_string not in self.dict_winddata:  # check key in dictionary - indexstring , as name
            #print('Create Wind data measurement object')
            year = int(token[0])
            assert year == year_file
            # print(wakati)
            lat = float(token[2])
            long = float(token[3])
            surface_alt = float(token[4])
            surface_u = float(token[5])
            surface_v = float(token[6])
            surface_rho = float(token[7])

            self.dict_winddata[index_string] = WindMeasurements(index_string,
                                                                year=year,
                                                                latitude=lat,  # read from data
                                                                longitude=long,
                                                                altitude=surface_alt,
                                                                surface_u=surface_u,
                                                                surface_v=surface_v,
                                                                surface_r=surface_rho,
                                                                min_altitude=self.min_altitude,  # object variables
                                                                max_altitude=self.max_altitude,
                                                                altitude_step_width=self.altitude_step_width)
        ialt = 30

        istart = 8
        offset = 0
        curr_alt_index = 0
        for k in range(ialt):
            ax = float(token[istart + offset])
            offset += 1
            if not (ax >= self.min_altitude and ax <= self.max_altitude):
                offset += 3
                # print('out of range ax: ', ax)
                continue

            ux = float(token[istart + offset])
            offset += 1
            vx = float(token[istart + offset])
            offset += 1
            rx = float(token[istart + offset])
            offset += 1

            #windspeed_final= self.dict_winddata[index_string].windspeed[day, curr_alt_index] #output 0 (when called 1st time)
            windspeed_final = np.sqrt(ux ** 2 + vx ** 2)
            self.dict_winddata[index_string].windspeed[day-1, curr_alt_index] = windspeed_final
            #print(windspeed_final)

            #windpower_final = self.dict_winddata[index_string].windpower[day, curr_alt_index]
            windpower_final = 0.5 * (rx * windspeed_final ** 3)
            self.dict_winddata[index_string].windpower[day-1, curr_alt_index] =windpower_final

            #print(self.dict_winddata[index_string])
            if len(self.dict_winddata[index_string].altitude_map) <= curr_alt_index:
                self.dict_winddata[index_string].altitude_map.append( round(ax,3) )

            curr_alt_index += 1
        print(self.dict_winddata[index_string].altitude_map)

    def load(self):
        # extract year, day from file name : DAILY+WIND+2007_015_relH.dat
        for f_name in self.windfiles:
            r = r'(\d+)'  # return digit -finds everything that is made out of digits (\d for digit)
            re_res = re.findall(r, f_name)
            assert  not len(re_res)  > 3

            if len(re_res) == 2 :
                year  = int(re_res[0])
                day   = int(re_res[1])

            if len(re_res) == 3:
                assert re_res[0] == re_res[1]
                year  = int(re_res[1])
                day   = int(re_res[2])



            with open(f_name, "r")  as f:
                n = 0
                for line in iter(f):
                    if n >= 2:
                        self.parse_line(line=line, year_file=year, day=day)

                    n += 1
                    # return dic_winddata

    def save_WindMeasuremnts(self):
        for index_string in self.dict_winddata:
            self.dict_winddata[index_string].save()



if __name__ == '__main__':
    print("test Wind_data_loader")
    print(np.__version__)

    # -----------------
    conf.npz_folder_path = conf.npz_folder_test_path



    wind_at_somewhere = WindMeasurements("foo", 11.2, 44.1, 0.1, 2017)
    # print(wind_at_somewhere)

    dates = wind_at_somewhere.get_list_of_dates_numpy()


    #print(len(dates))

    #print(dates)
    ind = 3
    alt = conf.index_to_altitude(ind)
    print("ind -> altitude: ", ind, "->", alt )

    wind_sum = WindMeasurements().load(WindMeasurements.createfilename(2007, 46.0, 3.0))

    print( wind_sum.sum_power(2))
    print( wind_sum.sum_power(1))

    print(wind_sum.windpower.shape)
    # fname = wind_at_somewhere.createfilename(2007 , 56.5 , 3.5)
    # print(fname)

    # wind_at_somewhere.save()

     #wind2 = WindMeasurements().load(WindMeasurements.createfilename(2017,11.2,44.1))

    # print(wind2)

    #wloader = WindDataConverter( conf.wind_data_test_globstring )
    #wdict = wloader.load()

    #wloader.save_WindMeasuremnts()

    #indata = WindMeasurements().load(WindMeasurements.createfilename(2007, 46.0, 3.0))
    #print ("am:", indata.altitude_map)

    w = WindMeasurements().load(conf.connected_filename(46.0, 3.0))

    #print(w)  #connected_filename(lat, long):



    print(w.windpower.shape)