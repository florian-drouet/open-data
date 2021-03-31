from func.geopandas import geopandas_dataviz
from func.prepare_data import prepare_data_hospit
import datetime

if __name__ == '__main__':

    input1 = input("Do you want to display data at a particular date ? [Y/N] ")
    if input1.lower() == "y":
        success = False
        while success==False:
            input2 = input("What is this date ? (DD/MM/YYYY) ")        
            try:
                study_day = datetime.datetime.strptime(input2, '%d/%m/%Y').date()
                success = True
            except:
                print("Wrong date format, please try again.")
                success = False
    else:
        # Fix-me : change to yesterday's date
        study_day = datetime.date.today() - datetime.timedelta(days=1)

    #study_day = datetime.date(2020,11,7)
    data = prepare_data_hospit(study_day)
    viz = geopandas_dataviz(size=10, title=f'Covid hospitalizations per 10000 inhabitants per department on {study_day.strftime("%d-%m-%Y")}')
    viz.plot(dataframe=data, plot_column='hospit_relative', cmap='plasma', shrink=0.65)