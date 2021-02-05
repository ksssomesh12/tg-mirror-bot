import os
import pickle
import logging

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from magic import Magic
from . import reformatter
from .dynamic import fileIdDict

LOGGER = logging.getLogger(__name__)


def file_dat(fileName: str):
    dat = open(fileName, 'r').read().replace(' = ', '\n').split('\n')
    env_name = []
    env_value = []
    i = 0
    while i <= ((dat.__len__() / 2) - 1):
        env_name.append(dat[i * 2])
        env_value.append(dat[(i * 2) + 1])
        i += 1
    return env_name, env_value


def update_dat(fileName: str, file_name_ch: str, new_env_value: str):
    reformatter.handler(fileName)
    env_name, env_value = file_dat(fileName)
    i = 0
    while i <= (env_name.__len__() - 1):
        if env_name[i] == file_name_ch.upper().replace('.', '_'):
            env_value[i] = new_env_value
        else:
            pass
        i += 1
    dat_new = ''
    i = 0
    while i <= (env_name.__len__() - 1):
        dat_new = dat_new + env_name[i] + ' = ' + env_value[i] + '\n'
        i += 1
    open(fileName, 'w').write(dat_new)


def authorize(token_file: str):
    creds = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            LOGGER.info('Token Expired')
            exit(1)
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    return build(serviceName='drive', version='v3', credentials=creds, cache_discovery=False)


def buildSync(fileName):
    service = authorize(token_file='token.pickle')
    fileMimetype = Magic(mime=True).from_file(fileName)
    fileMetadata = {'name': fileName, 'mimeType': fileMimetype}
    mediaBody = MediaFileUpload(filename=fileName, mimetype=fileMimetype, resumable=False)
    return service, fileMetadata, mediaBody


def filePatch(service, fileId, fileMetadata, mediaBody):
    fileSync = service.files().update(fileId=fileId, body=fileMetadata, media_body=mediaBody).execute()
    return fileSync


def fileReUpload(service, fileName, fileId, fileMetadata, mediaBody):
    fileMetadata['parents'] = [os.environ['CONFIG_PARENT_ID']]
    fileSync = service.files().create(body=fileMetadata, media_body=mediaBody).execute()
    service.files().delete(fileId=fileId).execute()
    update_fileid(fileName, fileSync)
    return fileSync


def update_fileid(fileName, fileSync):
    fileidName = 'fileid.env'
    update_dat(fileidName, fileName, fileSync['id'])
    fileidId = fileIdDict[fileidName.upper().replace('.', '_')]
    service, fileMetadata, mediaBody = buildSync(fileidName)
    fileidSync = filePatch(service, fileidId, fileMetadata, mediaBody)
    LOGGER.info(f"Updated 'fileid.env' - {fileidSync['id']}")


def handler(fileName: str, fileId: str, usePatch: bool):
    service, fileMetadata, mediaBody = buildSync(fileName)
    if usePatch:
        fileSync = filePatch(service, fileId, fileMetadata, mediaBody)
    else:
        fileSync = fileReUpload(service, fileName, fileId, fileMetadata, mediaBody)
    result_str = f"Synced: [{fileName}] [{os.path.getsize(fileName)} bytes] [{fileSync['id']}]"
    LOGGER.info(result_str)
    return result_str
