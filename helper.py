import numpy as np
import datetime as dt
import project_config as conf
#from wind_data import WindMeasurements

def weib(x,n,a):
    return (a / n) * (x/n)**(a-1)*np.exp(-(x/n)**a)
    

def moving_average(a, n):
    b = np.pad(a, n, 'edge')
    #b = np.pad(a, n, 'constant')
    #print(b)
    ret = np.cumsum(b, dtype=np.float64)
    ret[n:] = ret[n:]-ret[:-n]
    #print(ret)
    #print(len(ret[n - 1: -n  -1]), " == ",len(a)  )
    assert(len(ret[n - 1: -n -1]) == len(a) )

    return ret[n - 1: -n - 1] / n

def doy_to_date( day_of_year, year):
    ''' doy -> day of year'''
    return dt.date(year, 1, 1) + dt.timedelta(day_of_year)

def date_to_doy( d ):
    ''' doy -> day of year'''
    assert isinstance(d, dt.datetime ) or isinstance(d, dt.date )
    return d.timetuple().tm_yday

def altitude_to_int(alt):
    return int(alt * 10)


def coord_to_indices(lat, long):
    ## convert coordinate to index for array. either per formula or map however you like
    # example: (46.0, 3.0) -> (0, 0) and (46.5, 3.5) -> (1, 1)

    index_lat = (lat- conf.start_lat)* conf.coord_factor
    index_long = (long-conf.start_long)*conf.coord_factor

    assert index_lat < conf.num_locations_lat
    assert index_long < conf.num_locations_long

    assert index_lat >= 0
    assert index_long >= 0


    return (int(index_lat), int(index_long))

def indices_to_coords(index_lat, index_long):
    ## convert index to coordinate for array
    # example: (0, 0) -> (46.0, 3.0)
    lat = conf.start_lat + (index_lat * conf.coord_step)
    long = conf.start_long + (index_long * conf.coord_step)
    return (lat, long)


def get_grid():
    gridlat = np.ndarray( conf.num_locations_lat, dtype=np.float64 )
    gridlong = np.ndarray( conf.num_locations_long, dtype=np.float64 )

    for ilat in range(conf.num_locations_lat):
        for ilong in range(conf.num_locations_long):
            lat, long = indices_to_coords(ilat, ilong)
            gridlat[ilat] = lat
            gridlong[ilong] = long
    return (gridlat, gridlong)

def save_maps(arrays, year="",  all_years=False, compress=False,):
    if all_years:
        filename = conf.get_map_all_filename()
    else:
        filename = conf.get_map_filename(year)
    print("save as: ", filename)

    if compress:
        np.savez_compressed(filename, **arrays)
    else:
        np.savez(filename, **arrays)

def load_maps( year="", all_years=False):
    if all_years:
        filename = conf.get_map_all_filename()
    else:
        filename = conf.get_map_filename(year)

    print("load from: ",filename)
    with  np.load(filename, allow_pickle=False) as data:
        print(data.keys())
        return dict(data)


def get_grid_roi(lat_start, lat_end, lon_start, lon_end):
    numlat = int(((lat_end)-lat_start)*2)+1    
    numlong = int(((lon_end)-lon_start)*2)+1
    print(numlat, numlong)
    gridlat = np.ndarray( numlat, dtype=np.float64 )
    gridlong = np.ndarray( numlong, dtype=np.float64 )
    
    for ilat in range(numlat):
        for ilong in range(numlong):
            lat, long = indices_to_coords(ilat, ilong)
            gridlat[ilat] = lat
            gridlong[ilong] = long
    return (gridlat, gridlong)

def get_roi(data, lat_start, lat_end, lon_start, lon_end):#region of intrest
    #up_left = coord_to_indices(lat_end, lon_start)
    #up_right = coord_to_indices(lat_end, lon_end)
    #lower_left = coord_to_indices(lat_start, lon_start)
    #lower_right = coord_to_indices(lat_start, lon_end)
    up_left = coord_to_indices(lat_start, lon_start)
    lower_right = coord_to_indices(lat_end, lon_end)

    #print(up_left)
    #print(lower_right)
    d = data[up_left[0]:lower_right[0]+1, up_left[1]:lower_right[1]+1]
    #print(d, up_left[0], lower_right[0]+1, up_left[1],lower_right[1]+1)
    return d
    
if __name__ == '__main__':
    data = np.ones((120,120), dtype=np.float64)
    print( data )
    grid = get_grid_roi(52.0, 54.0, 12.0, 14.0)
    print(grid)
    d = get_roi(data, 52.0, 54.0, 12.0, 14.0) 
    print(d)