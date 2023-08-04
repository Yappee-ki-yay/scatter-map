from part-1 import *
# СОЗДАДИМ КАРТИНКУ PNG
plt.style.use('default')
def inch_to_px(value):
    return value/96
area_list = df['area'].unique().tolist()
df['color']=df['area+cluster']
df['color'] = df['color'].apply(lambda x: dct_color[x])
for i in range(len(df['area'].unique())):
    fig, ax = plt.subplots(figsize=(inch_to_px(1600), inch_to_px(1600)))
    ax.set_title("Диаграмма рассеяния", fontsize=16)
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
