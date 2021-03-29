import datetime
import pandas as pd

class anonymous:
    
    def __init__(self):
        self.df_k = pd.DataFrame()
        self.df_l = pd.DataFrame()
        self.sizes = dict()
        self.execution_times = dict()
        
    def k_anonymous(self, dataframe, columns_k, k):
        begin = datetime.datetime.now()
        sizing = (dataframe.groupby(columns_k).size()>=k)
        k_inner_merge = sizing.loc[sizing==True].reset_index()
        self.df_k = pd.merge(df, k_inner_merge[columns_k], how="inner", on=columns_k)
        self.sizes['k_anonymisation (%)'] = 100-round(((len(dataframe)-len(self.df_k))/len(dataframe))*100)
        self.execution_times['k_anonymisation'] = f"K-anonymisation runtime is : {((datetime.datetime.now()-begin).microseconds)/1000}ms"
    
    def l_diversity(self, column_l, columns_k, l):
        begin = datetime.datetime.now()
        sizing = (self.df_k.groupby(columns_k).nunique()>=l).reset_index()
        l_inner_merge = sizing.loc[sizing[f'{column_l}']]
        self.df_l = pd.merge(self.df_k, l_inner_merge[columns_k], how="inner", on=columns_k)        
        
        if len(self.df_k) == 0:
            raise Exception("K-anonymous dataset is empty")
        else:
            self.sizes['l_diversity (%)'] = 100-round(((len(self.df_k)-len(self.df_l))/len(self.df_k))*100)
            self.execution_times['l_diversity'] = f"L-diversity runtime is : {((datetime.datetime.now()-begin).microseconds)/1000}ms"

    def make_anonymous(self, dataframe, columns_k: list, column_l: str, k: int, l: int):
        self.k_anonymous(dataframe, columns_k, k)
        self.l_diversity(column_l, columns_k, l)