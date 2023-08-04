import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df=pd.read_excel('Тестовое задание.xlsx')

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

# УДАЛЯЕМ ДУБЛИКАТЫ СТРОК В ОБЛАСТЯХ

df = df.drop_duplicates(['area', 'keyword']).reset_index(drop=True)  

# ЗАПОЛНИМ СЛОВАРЬ УНИКАЛЬНЫМИ ЦВЕТАМИ НА КАЖДУЮ КОМБИНАЦИЮ ОБЛАСТЬ-КЛАСТЕР
color_dct={}            
df['area+cluster'] = df['area']+df['cluster'].astype('str')
unique_arcluster_list = list(set(list(df['area+cluster'])))
for i in range(len(unique_arcluster_list)):
    color = (np.random.randint(100, 999)/1000, np.random.randint(100, 999)/1000, np.random.randint(100, 999)/1000)
    if color not in color_dct:
        color_dct[color] = unique_arcluster_list[i]
    else:
        while color in color_dct:
            color = (np.random.randint(100, 999)/1000, np.random.randint(100, 999)/1000, np.random.randint(100, 999)/1000)
        color_dct[color] = unique_arcluster_list[i]
dct_color = {}
def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
for value in color_dct.values():
    if value not in dct_color:
        dct_color[value] = get_key(color_dct, value)

df.sort_values(['area', 'cluster', 'cluster_name', 'count'], ascending=[True, True, True, False ])



# СОЗДАДИМ КАРТИНКУ PNG
plt.style.use('default')
def inch_to_px(value):
    return value/96
area_list = df['area'].unique().tolist()
df['color']=df['area+cluster']
df['color'] = df['color'].apply(lambda x: dct_color[x])
for i in range(len(df['area'].unique())):
    fig, ax = plt.subplots(figsize=(inch_to_px(1600), inch_to_px(1600)), figsize=(inch_to_px(1600), inch_to_px(1600)))
    ax.text(0.5, -0.1, f'Данные по области {area_list[i]}', transform = ax.transAxes)
    ax.set_xlabel("x", fontsize=14, color = 'black')        
    ax.set_ylabel("y", fontsize=14, color = 'black')
    keywords_list = df[df['area'].isin([area_list[i]])]['keyword'].tolist()
    for j in range(len(keywords_list)):
        if len(keywords_list[j]) > 10:
            keywords_list[j]=keywords_list[j].replace(' ','\n')
    for j in range(len(df[df['area'].isin([area_list[i]])]['color'].tolist())):
        ax.text(df[df['area'].isin([area_list[i]])]['x'].tolist()[j], df[df['area'].isin([area_list[i]])]['y'].tolist()[j], keywords_list[j], color = df[df['area'].isin([area_list[i]])]['color'].tolist()[j], fontsize=6, horizontalalignment='center')
    a=0
    for k in range(1, len(df[df['area'].isin([area_list[i]])]['color'].to_list())):
        if df[df['area'].isin([area_list[i]])]['color'].to_list()[k] != df[df['area'].isin([area_list[i]])]['color'].to_list()[k-1]:
            ax.scatter(df[df['area'].isin([area_list[i]])]['x'].tolist()[a:k], df[df['area'].isin([area_list[i]])]['y'].tolist()[a:k], color = tuple(list(df[df['area'].isin([area_list[i]])]['color'].tolist()[a])+[0.5]))
            a=k
    ax.scatter(df[df['area'].isin([area_list[i]])]['x'].tolist()[-1], df[df['area'].isin([area_list[i]])]['y'].tolist()[-1], color = tuple(list(df[df['area'].isin([area_list[i]])]['color'].tolist()[-1])+[0.5]))
    plt.legend(df[df['area'].isin([area_list[i]])]['cluster_name'].unique().tolist(), bbox_to_anchor=( 1 , 1 ), loc='upper left', borderaxespad= 0)
    for j in range(len(area_list)):
        area_list[i]=area_list[i].replace('\\','__')
    plt.savefig(f'{area_list[i]}.png')
