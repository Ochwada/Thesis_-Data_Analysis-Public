import project_config as conf
import wind_data as wd

if __name__ == '__main__':

    for year in range(2007, 2017):
        print(conf.get_data_globstring_for_year( year ))
        #wloader = wd.WindDataConverter(conf.get_data_globstring_for_year( year ))

        wloader = wd.WindDataConverter( conf.get_data_globstring_for_year(year) )
        wdict = wloader.load()

        wloader.save_WindMeasuremnts()