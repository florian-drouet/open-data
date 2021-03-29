import geopandas
import pandas as pd
from matplotlib import pyplot as plt

class geopandas_dataviz():
    '''
    Class used to visualize data per french department.
    Input :
        - dataframe : a dataframe indexed on french departments (type : str)
        - plot_column : the name of the column containing the data to plot (type : str)
        - size : the size of the graph (type : int)
        - title : the title to display (type : str)
        - (Optional) shrink to adapt the size of the legend box (type : float)
        - (Optional) idf, if set to True then displays only Ile-de-France region (type : boolean)
    Output :
        - matplotlib graph
    '''

    def __init__(self, size, title):
        self.geojson_file = geopandas.read_file('data/departements.json').set_index('code')
        self.liste_dpt_idf = ["75", "77", "78", "91", "92", "93", "94", "95"]
        self.geojson_idf = self.geojson_file.loc[self.geojson_file.index.isin(self.liste_dpt_idf)]
        self.data = pd.DataFrame()
        self.size = size
        self.title = title
        self.fig = None
        self.ax = None
    
    def preprocess(self, dataframe, idf):
        if idf == True:
            self.data = dataframe.reindex(self.geojson_idf.index)
        else:
            self.data = dataframe.reindex(self.geojson_file.index)
    
    def define_figure(self):
        self.fig = plt.figure(figsize=(self.size, self.size))
        self.ax = plt.gca()
        self.ax.set_title(self.title)
    
    def show_map(self, plot_column, shrink, idf, **kwargs):    
        if self.ax is None:
            self.ax = plt.gca()    

        pd.merge(self.geojson_file, self.data, left_index=True, right_index=True).plot(column=plot_column, legend=True, ax=self.ax, legend_kwds={'shrink': shrink}, **kwargs)
        if idf==True:
            self.geojson_idf.plot(ax=self.ax, facecolor='none', edgecolor='#888', linewidth=1)
        else:
            self.geojson_file.plot(ax=self.ax, facecolor='none', edgecolor='#888', linewidth=1)

        self.ax.axis('off')
        self.ax.set_facecolor('white')
        plt.show()
        
    def plot(self, dataframe, plot_column, shrink=0.7, idf=False, **kwargs):
        self.preprocess(dataframe, idf)
        self.define_figure()
        self.show_map(plot_column, shrink, idf, **kwargs)

def prepare_data_hospit(study_day):
    '''
    Prepare data for geopandas data visualization.
    Input :
        -d dataframe donnees_hospitalieres (source : Santé Publique France)
        - dataframe population par departement (source : SIDEP)
    Output :
        - Preprocessed dataframe to inject in geopandas_dataviz class
    '''
    # read SPF data
    dataframe = pd.read_csv("data/donnees-hospitalieres-covid19-2021-03-29-18h03.csv", sep=";", parse_dates=['jour'])
    # converts from datetime to date format
    dataframe['jour_date'] = dataframe.jour.dt.date
    # group by department and date and aggregate data as a sum
    dataframe_groupby = dataframe.groupby(by=['dep', 'jour_date']).sum().reset_index()
    # filter on study day
    dataframe_day = dataframe_groupby.loc[dataframe_groupby.jour_date==study_day]
    # set department as dataframe_day's index
    dataframe_day = dataframe_day.set_index('dep')

    # read SIDEP data
    sidep = pd.read_csv("data/sp-pe-tb-quot-dep-2021-03-29-18h20.csv", sep=";", parse_dates=['jour'], low_memory=False)
    # converts from datetime to date
    sidep['jour_date'] = sidep.jour.dt.date
    # filter on last available data, groupby and aggregate by sum
    print(sidep.jour_date.iloc[-1])
    sidep_day = sidep.loc[sidep.jour_date==sidep.jour_date.iloc[-1]].groupby(by=['dep']).sum()

    # merging SPF and SIDEP dataframe
    merged_data = pd.merge(dataframe_day, sidep_day, left_index=True, right_index=True).reset_index()
    # number of hospit and rea covid for a 1000 inhabitants
    print(merged_data.columns)
    merged_data['hospit_relative'] = merged_data.hosp.div(merged_data["pop"])*1000
    merged_data['rea_relative'] = merged_data.rea.div(merged_data["pop"])*1000
    return merged_data

def prepare_data_covidom(dataframe, groupby_column, agg_func):
    return dataframe.groupby(by=groupby_column).agg(agg_func)