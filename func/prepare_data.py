from datetime import datetime
import os
import pandas as pd

def get_data_from_data_gouv():
    '''
    Function used to load data from data.gouv.fr or from data folder (if data.gouv.fr is unreachable)
    '''
    last_modified = os.stat('data/data_hospit.csv').st_mtime
    if datetime.fromtimestamp(last_modified).date() != datetime.today().date():
        try:
            data_hospit = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7', sep=";", low_memory=False)
            data_sidep = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/19a91d64-3cd3-42fc-9943-d635491a4d76', sep=";", low_memory=False)
            data_hospit.to_csv('data/data_hospit.csv', sep=";")
            data_sidep.to_csv('data/data_sidep.csv', sep=";")
        except:
            print("### Cannot reach data.gouv.fr server : use old tables ! ###")        
    else:
        print('### Data up-to-date ! ###')
        data_hospit = pd.read_csv("data/data_hospit.csv", sep=";", parse_dates=['jour'])
        data_sidep = pd.read_csv("data/data_sidep.csv", sep=";", parse_dates=['jour'], low_memory=False)
    return data_hospit, data_sidep


def prepare_data_hospit(study_day):
    '''
    Prepare data for geopandas data visualization.
    Input :
        - dataframe donnees_hospitalieres (source : https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/)
        - dataframe population par departement (source : https://www.data.gouv.fr/fr/datasets/taux-dincidence-de-lepidemie-de-covid-19/)
    Output :
        - Preprocessed dataframe to inject in geopandas_dataviz class
    '''
    data_hospit, data_sidep = get_data_from_data_gouv()
    # converts from datetime to date format
    data_hospit['jour_date'] = data_hospit.jour.dt.date
    # group by department and date and aggregate data as a sum
    dataframe_groupby = data_hospit.groupby(by=['dep', 'jour_date']).sum().reset_index()
    # filter on study day
    dataframe_day = dataframe_groupby.loc[dataframe_groupby.jour_date==study_day]
    # set department as dataframe_day's index
    dataframe_day = dataframe_day.set_index('dep')

    # converts from datetime to date
    data_sidep['jour_date'] = data_sidep.jour.dt.date
    # filter on last available data, groupby and aggregate by sum
    if data_sidep.jour_date.iloc[-1] < study_day:
        day = data_sidep.jour_date.iloc[-1]
    else:
        day = study_day
    sidep_day = data_sidep.loc[data_sidep.jour_date==day].groupby(by=['dep']).sum()

    # merging SPF and SIDEP dataframe
    merged_data = pd.merge(dataframe_day, sidep_day, left_index=True, right_index=True).reset_index()
    # number of hospit and rea covid for a 1000 inhabitants
    merged_data['hospit_relative'] = merged_data.hosp.div(merged_data["pop"])*1000
    merged_data['rea_relative'] = merged_data.rea.div(merged_data["pop"])*1000
    # set index department
    merged_data = merged_data.set_index('dep')
    return merged_data