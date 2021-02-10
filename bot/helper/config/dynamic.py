import aria2p
import os
import logging
import time
from .load import load_env, file_bak
from . import reformatter

LOGGER = logging.getLogger(__name__)
aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))
if os.environ['DYNAMIC_CONFIG'] == 'true':
    DYNAMIC_CONFIG = True
else:
    DYNAMIC_CONFIG = False
fileIdDict = {}
configList = ['config.env', 'credentials.json', 'token.pickle']
configListAll = configList + ['config.env.bak', 'fileid.env']


def rm_dl(fileName: str):
    env_name = fileName.upper().replace('.', '_')
    if os.path.exists(f'{fileName}'):
        os.remove(f'{fileName}')
    else:
        pass
    fileIdDict[env_name] = f"{os.environ[env_name]}"
    gid = aria2.add_uris([f"https://docs.google.com/uc?export=download&id={fileIdDict[env_name]}"]).gid
    retry_status = 0
    while aria2.get_download(gid).status != 'complete' and retry_status != 10 * os.environ['DL_WAIT_TIME']:
        time.sleep(0.1)
        retry_status += 1
    if os.path.exists(fileName):
        LOGGER.info(f"Downloaded '{fileName}'")
        pass
    else:
        LOGGER.error(f'Config File Missing: {fileName} ...\n Exiting...')
        exit(1)


def handler():
    if DYNAMIC_CONFIG:
        reformatter.handler('dynamic.env')
        load_env('dynamic.env')
        rm_dl('fileid.env')
        reformatter.handler('fileid.env')
        load_env('fileid.env')
        for file in configList:
            rm_dl(file)
        if os.path.exists('config.env.bak') is not True:
            file_bak('config.env')
    else:
        LOGGER.info('Using Static Config, Instead of Dynamic Config')
        pass
    reformatter.handler('config.env')
    load_env('config.env')
