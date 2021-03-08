import os
import pickle
import logging

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from magic import Magic
from . import load
from . import reformatter
from .dynamic import fileIdDict

LOGGER = logging.getLogger(__name__)


def authorize(token_file: str):
    creds = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            LOGGER.info(f"'{token_file}' Expired, Please Update Manually")
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


def filePatch(service, fileName, fileId, fileMetadata, mediaBody):
    fileSync = service.files().update(fileId=fileId, body=fileMetadata, media_body=mediaBody).execute()
    return f"Synced: [{fileName}] [{os.path.getsize(fileName)} bytes]\n[{fileSync['id']}]"


def fileReUpload(service, fileName, fileId, fileMetadata, mediaBody):
    fileMetadata['parents'] = [os.environ['CONFIG_PARENT_ID']]
    fileSync = service.files().create(body=fileMetadata, media_body=mediaBody).execute()
    load.update_dat('fileid.env', fileName.upper().replace('.', '_'), fileSync['id'])
    service.files().delete(fileId=fileId).execute()
    return f"Synced: [{fileName}] [{os.path.getsize(fileName)} bytes]\n[{fileId}] -> [{fileSync['id']}]"


def file(fileName: str, fileId: str, useReformat: bool, usePatch: bool):
    if useReformat:
        reformatter.handler(fileName)
    else:
        pass
    service, fileMetadata, mediaBody = buildSync(fileName)
    if usePatch:
        return filePatch(service, fileName, fileId, fileMetadata, mediaBody)
    else:
        return fileReUpload(service, fileName, fileId, fileMetadata, mediaBody)


def handler(fileList: list):
    for fileName in fileList:
        if fileName.endswith('.env'):
            ifReformat = ifPatch = True
        else:
            ifReformat = ifPatch = False
        fileId = fileIdDict[fileName.upper().replace('.', '_')]
        result_file = file(fileName, fileId, usePatch=ifPatch, useReformat=ifReformat)
        LOGGER.info(result_file)
