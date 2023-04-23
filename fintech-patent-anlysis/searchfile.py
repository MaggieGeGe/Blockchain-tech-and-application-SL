from __future__ import print_function

import os.path
from google.cloud import language_v1
from google.cloud import api_keys_v2

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import csv
import io

#  权限设置
SCOPES = ['https://www.googleapis.com/auth/drive']

# 定义需要访问的 Google Drive 文件的 MIME 类型
MIME_TYPE_EXCEL = 'application/vnd.google-apps.spreadsheet' #表格

# 定义需要访问的 Google Drive 文件的名称
FILE_NAME = 'PCT_data'

#读取文件
FILE_LIST = {}



"""Shows basic usage of the Drive v3 API.
Prints the names and ids of the first 10 files the user has access to.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
        
    print('Files Found:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))
    
except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f'An error occurred: {error}')



def get_csv_files_from_folder(folder_id, mime_type):
    """
    从给定的Google Drive文件夹及其子文件夹中获取CSV文件
    """
    parents = service.files().list(q = f"name = '{FILE_NAME}'" ,fields="nextPageToken, files(id, name, mimeType,parents,createdTime)").execute()
    parents_info = parents.get('files',[])[0]
    parents_id = parents_info['id']
    
    results = service.files().list(
        q="'{}' in parents and trashed = false".format( parents_id),
        fields="nextPageToken, files(id, name,mimeType, createdTime)").execute()

    print((results))

    items = results.get('files', [])


    # 遍历文件夹中的文件和子文件夹
    for item in items:
        # 如果是文件夹，则递归调用该函数
        
        if item['mimeType'] == 'application/vnd.google-apps.folder':
           print('0')
           # get_csv_files_from_folder(item['id'], mime_type)
        else:
            # 如果文件是CSV文件，则打印文件名和创建时间，并读取CSV文件
            if item['name'].endswith('.csv'):
                print("File name: {}, Created Time: {}".format(item['name'], item['createdTime']))

                # 读取CSV文件
                file = service.files().get_media(fileId=item['id']).execute()
                content = file.decode('utf-8')
                csv_data = csv.reader(io.StringIO(content))
                FILE_LIST[item['name']] = csv_data
                print(FILE_LIST)
   
if __name__ == '__main__':

    
    
    get_csv_files_from_folder(FILE_NAME,MIME_TYPE_EXCEL)
    #print(FILE_LIST)


