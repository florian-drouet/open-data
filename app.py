import pandas as pd
from func.geopandas import geopandas_dataviz, prepare_data_hospit, prepare_data_covidom
import datetime

if __name__ == '__main__':

    study_day = datetime.date(2021,2,26)
    data = prepare_data_hospit(study_day)

    viz = geopandas_dataviz(size=10, title=f'Hospitalisation pour 1000 habitants par département le {study_day.strftime("%d-%m-%Y")}')
    viz.plot(dataframe=data, plot_column='hospit_relative', cmap='plasma', shrink=0.65)