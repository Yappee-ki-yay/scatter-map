import httplib2 
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pygsheets

# ДЛЯ НАЧАЛА СОЕДИНЯЕМСЯ С API GOOGLE SPREADSHEETS
CREDENTIALS_FILE = 'credentials.json'

# ЧИТАЕМ КЛЮЧИ ИЗ ФАЙЛА
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
# АВТОРИЗАЦИЯ В СИСТЕМЕ
httpAuth = credentials.authorize(httplib2.Http())
# ВЫБИРАЕМ РАБОТУ С ТАБЛИЦАМИ И 4 ВЕРСИЮ API 
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

# СОЗДАЁМ ЛИСТ, КУДА БУДЕМ ЗАПИСЫВАТЬ ДАННЫЕ
spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': 'Результат', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист №1',
                               'gridProperties': {'rowCount': 500, 'columnCount': 15}}}],
                               
}).execute()
# СОХРАНЯЕМ ИДЕНТИФИКАТОР СОЗДАННОГО ЛИСТА
spreadsheetId = spreadsheet['spreadsheetId']
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
# ВЫБИРАЕМ РАБОТУ С Google Drive И 3 ВЕРСИЮ API
driveService = googleapiclient.discovery.build('drive', 'v3', http = httpAuth)
# ОТКРЫВАЕМ ДОСТУП НА РЕДАКТИРОВАНИЕ
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'aseevgeny@gmail.com'},
    fields = 'id'
).execute()



# ГОТОВО!
# ПРИСТУПАЕМ К ОЧИСТКЕ И ОБРАБОТКЕ ИСХОДНЫХ ДАННЫХ
# ПОДГОТОВИМ ДАННЫЕ, ПРИВЕДЁМ ТИПЫ СТОЛБЦОВ, УДАЛИМ НЕВАЛИДНЫЕ СТРОКИ



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


# ЗАПИСЫВАЕМ ДАТАФРЕЙМ В GOOGLE SPREADSHEET
result = df.copy()
result = result.drop('area+cluster', axis=1)
def write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df):
    gc = pygsheets.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks_write = sh.worksheet_by_title(sheet_name)
    wks_write.clear('A1',None,'*')
    wks_write.set_dataframe(data_df, (1,1), encoding='utf-8', fit=True)
    wks_write.frozen_rows = 1
    wks_write.set_basic_filter()

write_to_gsheet(CREDENTIALS_FILE,spreadsheetId,'Лист №1',result)

# ЗАПИСАЛИ
