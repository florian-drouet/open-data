from func.geopandas import geopandas_dataviz
from func.prepare_data import prepare_data_hospit
import datetime

if __name__ == '__main__':

    study_day = datetime.date(2020,11,7)
    data = prepare_data_hospit(study_day)

    viz = geopandas_dataviz(size=10, title=f'Hospitalisation pour 1000 habitants par département le {study_day.strftime("%d-%m-%Y")}')
    viz.plot(dataframe=data, plot_column='rea_relative', cmap='plasma', shrink=0.65)