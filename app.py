import pandas as pd
from func.anonymity import anonymous

if __name__ == '__main__':
    data=[[75015, 'H', 75, 'diabete'],
          [92100, 'F', 60, 'cancer'],
          [75015, 'H', 60, 'cancer'],
          [75015, 'F', 68, 'cancer'],
          [75016, 'F', 84, 'cancer'],
          [75015, 'H', 72, 'asthma'],
          [75014, 'F', 74, 'asthma'],
          [92100, 'F', 60, 'cancer'],
          [92100, 'H', 68, 'cancer'],
          [92100, 'F', 55, 'cancer'],
          [46140, 'H', 94, 'diabete'],
          [77300, 'H', 68, 'diabete']]
    df = pd.DataFrame(data=data, columns=['department', 'gender', 'weight', 'comorbidities'])
    results = anonymous()
    results.make_anonymous(dataframe=df, columns_k=['department', 'gender'], column_l='comorbidities', k=3, l=2)
    print(results.df_k)
    print(results.df_l)