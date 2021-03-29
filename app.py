import pandas as pd
from func.geopandas import geopandas_dataviz

if __name__ == '__main__':
    df = pd.read_csv('./data/donnees-hospitalieres-nouveaux-covid19-2021-03-28-19h03.csv', sep=';')
    viz = geopandas_dataviz(size=10, title='Nombre total de réanimation par département')
    viz.plot(dataframe=df, groupby_column='dep', agg_func='sum', plot_column='incid_rea', cmap='plasma', shrink=0.65, idf=True)