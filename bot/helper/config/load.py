import os
from . import reformatter


def load_dat(fileName: str):
    dat = open(fileName, 'r').read().replace(' ', '').replace('=', '\n').split('\n')
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
    env_name, env_value = load_dat(fileName)
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


def load_dict(fileName: str):
    env_name, env_value = load_dat(fileName)
    i = 0
    dict = {}
    while i <= (env_name.__len__() - 1):
        dict[env_name[i]] = env_value[i]
        i += 1
    return dict


def load_env(fileName: str):
    env_dict = load_dict(fileName)
    for env in env_dict:
        if env_dict[env] != '':
            os.environ[env] = env_dict[env]
        else:
            pass
