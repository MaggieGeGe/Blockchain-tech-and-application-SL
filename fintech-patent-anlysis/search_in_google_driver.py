import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import io
import csv

# 定义 API 客户端名称和版本
API_NAME = 'drive'
API_VERSION = 'v3'

# 定义需要访问的 Google Drive 文件的 MIME 类型
MIME_TYPE_EXCEL = 'application/vnd.google-apps.spreadsheet' #表格

# 定义需要访问的 Google Drive 文件的名称
FILE_NAME = 'PCT_data'

# 定义 API 访问范围
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# 定义 API 密钥文件的名称(new json for windows application)
API_KEY_FILE = '/Users/zhangyunmengge/Desktop/myproject/Blockchain-tech-and-application-SL/fintech-patent-anlysis/credi.json'


FILE_LIST = {}

#creds = Credentials.from_authorized_user_file(API_KEY_FILE)
# 检查是否有 API 密钥文件

if os.path.exists(API_KEY_FILE):
    # 加载 API 密钥文件
    with open(API_KEY_FILE) as f:
        api_key = json.load(f)

    # 检查是否需要刷新 API 访问令牌
    if api_key.get('token') and api_key.get('refresh_token'):
        # 刷新 API 访问令牌
        credentials = Credentials.from_authorized_user_info(api_key)
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
    else:
        # 使用 API 密钥进行身份验证
        flow = InstalledAppFlow.from_client_config(api_key, SCOPES)
        credentials = flow.run_local_server(port=0)

# 创建 API 客户端
service = build(API_NAME, API_VERSION, credentials=credentials)

    # # 搜索 Google Drive 中的文件
    # results = service.files().list(q=f"name='{FILE_NAME}'",
    #                                fields='files(id)').execute()


# #find all files

# results = service.files().list(
#     pageSize=10, fields="nextPageToken, files(id, name)").execute()
# items = results.get('files', [])

# if not items:
#     print('No files found.')
# else:
#     print('Files:')
#     for item in items:
#         print(u'{0} ({1})'.format(item['name'], item['id']))


def get_csv_files_from_folder(folder_id, mime_type):
    """
    从给定的Google Drive文件夹及其子文件夹中获取CSV文件
    """
    results = service.files().list(
        q="mimeType='{}' and parents in '{}'".format(mime_type, folder_id),
        fields="nextPageToken, files(id, name, createdTime)").execute()

    print(len(results))

    items = results.get('files', [])


    # 遍历文件夹中的文件和子文件夹
    for item in items:
        # 如果是文件夹，则递归调用该函数
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            get_csv_files_from_folder(item['id'], mime_type)
        else:
            # 如果文件是CSV文件，则打印文件名和创建时间，并读取CSV文件
            if item['name'].endswith('.csv'):
                print("File name: {}, Created Time: {}".format(item['name'], item['createdTime']))

                # 读取CSV文件
                file = service.files().get_media(fileId=item['id']).execute()
                content = file.decode('utf-8')
                csv_data = csv.reader(io.StringIO(content))
                FILE_LIST[item['name']] = csv_data
                

# 调用函数以获取文件夹中的CSV文件
get_csv_files_from_folder(FILE_NAME, MIME_TYPE_EXCEL)
print(FILE_LIST.keys())
