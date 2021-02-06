import os
import pickle
import logging

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from magic import Magic
from . import load
from .dynamic import fileIdDict
from bot.helper.telegram_helper.message_utils import sendMessage

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
            LOGGER.info("'token.pickle' Expired, Please Update Manually")
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


def result_string(fileName, fileSync):
    return f"Synced: [{fileName}] [{os.path.getsize(fileName)} bytes] [{fileSync['id']}]"


def filePatch(service, fileId, fileMetadata, mediaBody):
    fileSync = service.files().update(fileId=fileId, body=fileMetadata, media_body=mediaBody).execute()
    return fileSync


def fileReUpload(service, fileName, fileId, fileMetadata, mediaBody):
    fileMetadata['parents'] = [os.environ['CONFIG_PARENT_ID']]
    fileSync = service.files().create(body=fileMetadata, media_body=mediaBody).execute()
    service.files().delete(fileId=fileId).execute()
    upd_fileid_str = update_fileid_env(fileName, fileSync)
    return fileSync, upd_fileid_str


def update_fileid_env(fileName, fileSync):
    fileidName = 'fileid.env'
    load.update_dat(fileidName, fileName, fileSync['id'])
    fileidId = fileIdDict[fileidName.upper().replace('.', '_')]
    service, fileMetadata, mediaBody = buildSync(fileidName)
    fileidSync = filePatch(service, fileidId, fileMetadata, mediaBody)
    return result_string(fileidName, fileidSync)


def handler(fileName: str, fileId: str, usePatch: bool, update, context):
    sync_msg = sendMessage(f"Syncing '{fileName}' to Google Drive...", context.bot, update)
    service, fileMetadata, mediaBody = buildSync(fileName)
    if usePatch:
        fileSync, upd_fileid_res = filePatch(service, fileId, fileMetadata, mediaBody), ''
    else:
        fileSync, upd_fileid_res = fileReUpload(service, fileName, fileId, fileMetadata, mediaBody)
    result_str = result_string(fileName, fileSync)
    LOGGER.info(result_str)
    sync_msg.edit_text(result_str)
    if upd_fileid_res != '':
        LOGGER.info(upd_fileid_res)
        sendMessage(upd_fileid_res, context.bot, update)
    else:
        pass
    return
