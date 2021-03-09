import os
import pickle
import re
import shutil
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from magic import Magic


def reformatter(fileName: str):
    formatted = ''
    for line in open(fileName, 'r').readlines():
        commented = re.findall("^#", line)
        newline = re.findall("^\n", line)
        if not commented and not newline:
            formatted = formatted + line
    if open(fileName, 'r').read() == formatted:
        pass
    else:
        open(fileName, 'w').write(formatted)
        print(f"Reformatted '{fileName}'")
    return


def file_bak(fileName: str):
    cwd = os.getcwd()
    fileBakName = fileName + '.bak'
    shutil.copy(os.path.join(cwd, fileName), os.path.join(cwd, fileBakName))
    if open(fileName, 'r').read() == open(fileBakName, 'r').read():
        print(f"Copied: '{fileName}' -> '{fileBakName}'")
    else:
        print(f"Error Copying '{fileName}'")
        exit(1)


def load_ids(fileName: str):
    lines = open(fileName, 'r').readlines()
    env_value = []
    for i in range(len(lines)):
        line_dat = lines[i].replace('\n', '').replace('"', '').split(' = ')
        env_value.append(line_dat[1])
    return env_value


def authorize(token_file: str = 'token.pickle'):
    creds = None
    OAUTH_SCOPE = ["https://www.googleapis.com/auth/drive"]
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Generating 'token.pickle'...\nPlease Authorize the AppFlow...")
            time.sleep(1)
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', OAUTH_SCOPE)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        print("Generated 'token.pickle'")
    return creds


def fileDownload(fileId: str):
    global service
    fileName = service.files().get(fileId=fileId).execute()['name']
    fileOp = service.files().get_media(fileId=fileId).execute()
    open(fileName, 'wb').write(fileOp)
    print(f"Downloaded '{fileName}'")


def fileUpload(fileName: str):
    global service, CONFIG_PARENT_ID
    fileMimetype = Magic(mime=True).from_file(fileName)
    fileMetadata = {'name': fileName, 'mimeType': fileMimetype, 'parents': [CONFIG_PARENT_ID]}
    mediaBody = MediaFileUpload(filename=fileName, mimetype=fileMimetype, resumable=False)
    fileOp = service.files().create(body=fileMetadata, media_body=mediaBody).execute()
    print(f"Uploaded: [{fileOp['id']}] [{fileName}] [{os.path.getsize(fileName)} bytes]")
    return fileOp['id']


def filePatch(fileName: str, fileId: str):
    global service
    fileMimetype = Magic(mime=True).from_file(fileName)
    fileMetadata = {'name': fileName, 'mimeType': fileMimetype}
    mediaBody = MediaFileUpload(filename=fileName, mimetype=fileMimetype, resumable=False)
    fileOp = service.files().update(fileId=fileId, body=fileMetadata, media_body=mediaBody).execute()
    print(f"Synced: [{fileOp['id']}] [{fileName}] [{os.path.getsize(fileName)} bytes]")
    return fileOp['id']


def fileDelete(fileId: str):
    global service
    fileName = service.files().get(fileId=fileId).execute()['name']
    service.files().delete(fileId=fileId).execute()
    print(f"Deleted: [{fileId}] [{fileName}]")


def handler():
    global fileList, old_ids, CONFIG_PARENT_ID, UPDATE_CONFIG
    if os.path.exists('dynamic.env'):
        os.remove('dynamic.env')
    if os.path.exists('fileid.env'):
        os.remove('fileid.env')
    file_bak(fileList[0])
    reformatter(fileList[0])
    fileid_dat = f'CONFIG_PARENT_ID = "' + CONFIG_PARENT_ID + '"\n'
    for fileName in fileList[0:5]:
        fileId = fileUpload(fileName)
        fileid_dat = fileid_dat + fileName.upper().replace('.', '_') + ' = "' + fileId + '"\n'
    open(fileList[5], 'w').write(fileid_dat)
    reformatter(fileList[5])
    dynamic_dat = f'DL_WAIT_TIME = "' + input('Enter DL_WAIT_TIME (default is 5): ') + '"\n'
    if UPDATE_CONFIG:
        dynamic_dat = dynamic_dat + fileList[5].upper().replace('.', '_') + ' = "' + filePatch(fileList[5], old_ids[1]) + '"\n'
    if not UPDATE_CONFIG:
        dynamic_dat = dynamic_dat + fileList[5].upper().replace('.', '_') + ' = "' + fileUpload(fileList[5]) + '"\n'
    open(fileList[6], 'w').write(dynamic_dat)
    reformatter(fileList[6])
    if UPDATE_CONFIG:
        filePatch(fileList[6], old_ids[0])
    if not UPDATE_CONFIG:
        fileUpload(fileList[6])
    for file in fileList[1:6]:
        os.remove(file)


credentials = authorize()
fileList = ['config.env', 'config.env.bak', 'credentials.json', 'token.pickle', 'netrc', 'fileid.env', 'dynamic.env']
UPDATE_CONFIG = False
service = build(serviceName='drive', version='v3', credentials=credentials, cache_discovery=False)
if input('Do You Want to Use Dynamic Config? (y/n): ').lower() == 'y':
    if input('Do You Want to Update Existing Config? (y/n): ').lower() == 'y':
        UPDATE_CONFIG = True
        old_ids = [input("Enter FileId of 'dynamic.env': ")]
        fileDownload(old_ids[0])
        old_ids.append(load_ids('dynamic.env')[1])
        fileDownload(old_ids[1])
        CONFIG_PARENT_ID = load_ids('fileid.env')[0]
        old_ids = old_ids + load_ids('fileid.env')[1:6]
        handler()
        if input('Do You Want to Delete Old Config Files? (y/n): ').lower() == 'y':
            for fileid in old_ids[2:7]:
                fileDelete(fileid)
    else:
        CONFIG_PARENT_ID = input('Enter Google Drive Parent Folder ID: ')
        handler()
print('Setup Completed')
exit(0)

# sample - dynamic.env
# --- BEGINS --- #
# FILEID_ENV = ""
# DL_WAIT_TIME = "5"
# --- ENDS --- #

# sample - fileid.env
# --- BEGINS --- #
# CONFIG_PARENT_ID = ""
# CONFIG_ENV = ""
# CREDENTIALS_JSON = ""
# TOKEN_PICKLE = ""
# --- ENDS --- #
