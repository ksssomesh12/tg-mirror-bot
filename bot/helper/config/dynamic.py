import os
import logging
import time
import aria2p
from .load import load_env
from . import reformatter

LOGGER = logging.getLogger(__name__)
aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))
fileIdDict = {}


def rm_dl(file_name: str):
    env_name = file_name.upper().replace('.', '_')
    if os.path.exists(f'{file_name}'):
        os.remove(f'{file_name}')
    else:
        pass
    fileIdDict[f'{env_name}'] = f"{os.environ[f'{env_name}']}"
    gid = aria2.add_uris([f"https://docs.google.com/uc?export=download&id={fileIdDict[env_name]}"]).gid
    retry_status = 0
    while aria2.get_download(gid).status != 'complete' and retry_status != 10 * os.environ['DL_WAIT_TIME']:
        time.sleep(0.1)
        retry_status += 1
    if os.path.exists(file_name):
        LOGGER.info(f"Downloaded '{file_name}'")
        pass
    else:
        LOGGER.error(f'Config File Missing: {file_name} ...\n Exiting...')
        exit(1)


def handler():
    if os.environ['DYNAMIC_CONFIG'] == 'true':
        reformatter.handler('dynamic.env')
        load_env('dynamic.env')
        rm_dl('fileid.env')
        load_env('fileid.env')
        file_list = ['config.env', 'credentials.json', 'token.pickle']
        for i in file_list:
            rm_dl(i)
    else:
        LOGGER.info('Using Static Config, Instead of Dynamic Config')
        pass
