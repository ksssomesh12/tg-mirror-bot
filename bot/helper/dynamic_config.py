import os
import logging
import time
import aria2p
from dotenv import load_dotenv

LOGGER = logging.getLogger(__name__)

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret="",
    )
)


def helper():
    if os.environ['DYNAMIC_CONFIG'] == 'true':
        load_dotenv('dynamic_config.env')
        env_dict = {}

        def rm_dl(file_name: str):
            env_name = (file_name.upper()).replace('.', '_')
            if os.path.exists(f'{file_name}'):
                os.remove(f'{file_name}')
                LOGGER.info(f'Removed Redundant File: {file_name}')
            else:
                pass
            env_dict[f'{env_name}'] = f"{os.environ[f'{env_name}']}"
            aria2.add_uris([f"https://docs.google.com/uc?export=download&id={env_dict[env_name]}"])
            time.sleep(5)
            if os.path.exists(f'{file_name}'):
                LOGGER.info(f'Downloaded Config File: {file_name}')
            else:
                LOGGER.error(f'Config File Missing: {file_name} ...\n Exiting...')
                exit(1)

        file_list = ['config.env', 'credentials.json', 'token.pickle']
        for i in file_list:
            rm_dl(i)
    else:
        pass
