import pandas as pd
import numpy as np
import gspread as gc
import matplotlib.pyplot as plt

df=pd.read_excel('Тестовое задание.xlsx') #ПОДГОТОВИМ ДАННЫЕ, ПРИВЕДЁМ ТИПЫ СТОЛБЦОВ, УДАЛИМ НЕВАЛИДНЫЕ СТРОКИ

df = df.drop('good (1)', axis=1)
df=df.dropna().reset_index(drop=True)

df=df.astype({'area':'str','cluster':'int64','cluster_name':'str','keyword':'str','count':'int64'},errors = 'ignore')
df['x']=pd.to_numeric(df['x'],errors='coerce')
df['y']=pd.to_numeric(df['y'],errors='coerce')

df['cluster'] = np.where(df['cluster']*0==0, df['cluster'], None)
df['count'] = np.where(df['count']*0==0, df['count'], None)
df['x'] = np.where(df['x']*0==0.0, df['x'], None)
df['y'] = np.where(df['y']*0==0.0, df['y'], None)
df=df.dropna().reset_index(drop=True)

df = df.drop_duplicates(['area', 'keyword']).reset_index(drop=True)  #УДАЛЯЕМ ДУБЛИКАТЫ СТРОК В ОБЛАСТЯХ

color_dct={}            #ЗАПОЛНИМ СЛОВАРЬ УНИКАЛЬНЫМИ ЦВЕТАМИ НА КАЖДУЮ КОМБИНАЦИЮ ОБЛАСТЬ-КЛАСТЕР
df['area+cluster'] = df['area']+df['cluster'].astype('str')
unique_arcluster_list = list(set(list(df['area+cluster'])))
for i in range(len(unique_arcluster_list)):
    color = (np.random.random (), np.random.random (), np.random.random ())
    if color not in color_dct:
        color_dct[color] = unique_arcluster_list[i]
    else:
        while color in color_dct:
            color = (np.random.random (), np.random.random (), np.random.random ())
        color_dct[color] = unique_arcluster_list[i]

df.sort_values(['area', 'cluster', 'cluster_name', 'count'], ascending=[True, True, True, False ])
