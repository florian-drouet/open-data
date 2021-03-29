import pandas as pd
from func.geopandas import geopandas_dataviz
import datetime

if __name__ == '__main__':

    study_day = datetime.date(2021,2,26)

    df = pd.read_csv("data/donnees-hospitalieres-covid19-2021-03-29-18h03.csv", sep=";", parse_dates=['jour'])
    df['jour_date'] = df.jour.dt.date
    df_groupby = df.groupby(by=['dep', 'jour_date']).sum().reset_index()
    df_day = df_groupby.loc[df_groupby.jour_date==study_day]
    df_day = df_day.set_index('dep')

    sidep = pd.read_csv("data/sp-pe-tb-quot-dep-2021-03-29-18h20.csv", sep=";", parse_dates=['jour'], low_memory=False)
    sidep['jour_date'] = sidep.jour.dt.date
    sidep_day = sidep.loc[sidep.jour_date==study_day].groupby(by=['dep']).sum()

    merged_data = pd.merge(df_day, sidep_day, left_index=True, right_index=True).reset_index()
    merged_data['hospit_relative'] = merged_data.hosp.div(merged_data["pop"])*1000

    #df = pd.read_csv('data/donnees-hospitalieres-nouveaux-covid19-2021-03-28-19h03.csv', sep=';')
    viz = geopandas_dataviz(size=10, title=f'Hospitalisation pour 1000 habitants par département le {study_day.strftime("%d-%m-%Y")}')
    viz.plot(dataframe=merged_data, groupby_column='dep', agg_func='sum', plot_column='hospit_relative', cmap='plasma', shrink=0.65)