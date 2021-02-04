import os
import pickle
import logging

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from magic import Magic

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
            LOGGER.info('Token Expired')
            exit(1)
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    return build(serviceName='drive', version='v3', credentials=creds, cache_discovery=False)


def handler(file_name: str, file_id: str):
    file_mimetype = Magic(mime=True).from_file(file_name)
    file_metadata = {'name': file_name, 'mimeType': file_mimetype}
    media_body = MediaFileUpload(filename=file_name, mimetype=file_mimetype, resumable=False)
    service = authorize(token_file='token.pickle')
    file_upload = service.files().update(fileId=file_id, body=file_metadata, media_body=media_body).execute()
    result_str = f"[{file_name}] [{os.path.getsize(file_name)} bytes] [{file_upload['id']}]"
    LOGGER.info(result_str)
    return result_str
