import os
import logging
from .load import load_env
from . import reformatter
from .subproc import ariaDaemonStart, dl, netrc

LOGGER = logging.getLogger(__name__)

if os.path.exists('dynamic.env'):
    os.environ['DYNAMIC_CONFIG'] = 'true'
    DYNAMIC_CONFIG = True
else:
    os.environ['DYNAMIC_CONFIG'] = 'false'
    DYNAMIC_CONFIG = False
fileIdDict = {}
configList = ['config.env', 'config.env.bak', 'credentials.json', 'token.pickle', 'netrc', 'fileid.env']


def rm_dl(fileName: str):
    env_name = fileName.upper().replace('.', '_')
    if os.path.exists(f'{fileName}'):
        os.remove(f'{fileName}')
    fileIdDict[env_name] = f"{os.environ[env_name]}"
    dl(f"https://docs.google.com/uc?export=download&id={fileIdDict[env_name]}", fileName)
    if os.path.exists(fileName):
        LOGGER.info(f"Downloaded '{fileName}'")
        pass
    else:
        LOGGER.error(f"Config File Missing: '{fileName}' ...\n Exiting...")
        exit(1)


def handler():
    if DYNAMIC_CONFIG:
        reformatter.handler('dynamic.env')
        load_env('dynamic.env')
        rm_dl('fileid.env')
        reformatter.handler('fileid.env')
        load_env('fileid.env')
        for file in configList[0:5]:
            rm_dl(file)
    if not DYNAMIC_CONFIG:
        LOGGER.info('Using Static Config, Instead of Dynamic Config')
        os.environ['DL_WAIT_TIME'] = '5'
    reformatter.handler('config.env')
    load_env('config.env')
    netrc()
    ariaDaemonStart()
