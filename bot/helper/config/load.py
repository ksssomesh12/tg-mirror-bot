import logging
import os
import shutil
from . import reformatter

LOGGER = logging.getLogger(__name__)


def load_dat(fileName: str):
    dat = open(fileName, 'r').read().replace(' ', '').replace('=', '\n').split('\n')
    env_name = []
    env_value = []
    for i in range((int(len(dat) / 2))):
        env_name.append(dat[i * 2])
        env_value.append(dat[(i * 2) + 1])
    return env_name, env_value


def update_dat(fileName: str, ch_key: str, ch_value: str):
    reformatter.handler(fileName)
    env_name, env_value = load_dat(fileName)
    for i in range(len(env_name)):
        if env_name[i] == ch_key:
            env_value[i] = ch_value
            pass
    dat_new = ''
    for i in range(len(env_name)):
        dat_new = dat_new + env_name[i] + ' = ' + env_value[i] + '\n'
    open(fileName, 'w').write(dat_new)


def load_dict(fileName: str):
    env_name, env_value = load_dat(fileName)
    env_dict = {}
    for i in range(len(env_name)):
        env_dict[env_name[i]] = env_value[i]
    return env_dict


def load_env(fileName: str):
    env_dict = load_dict(fileName)
    for env in env_dict:
        if env_dict[env] != '':
            os.environ[env] = env_dict[env]


def file_bak(fileName: str):
    cwd = os.getcwd()
    fileBakName = fileName + '.bak'
    shutil.copy(os.path.join(cwd, fileName), os.path.join(cwd, fileBakName))
    if open(fileName, 'r').read() == open(fileBakName, 'r').read():
        LOGGER.info(f"Copied: '{fileName}' -> '{fileBakName}'")
        return fileBakName
    else:
        LOGGER.info(f"Error Copying '{fileName}'")
        exit(1)
