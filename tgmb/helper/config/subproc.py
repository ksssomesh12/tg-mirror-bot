import logging
import os
import subprocess
import time

LOGGER = logging.getLogger(__name__)

ariaDaemon: subprocess.Popen


def ariaDaemonStart():
    global ariaDaemon
    ariaScriptName = 'aria.sh'
    ariaLogName = 'aria_log.txt'
    trackerslistName = 'trackerslist.txt'
    for file in [ariaScriptName, ariaLogName, trackerslistName]:
        if os.path.exists(file):
            os.remove(file)
    dl(os.environ['TRACKERSLIST'], trackerslistName)
    LOGGER.info(f"Generating '{ariaScriptName}'...")
    dat = (
        f'#!/bin/bash' '\n' '\n'
        f'aria2c '
        f'--daemon '
        f'--enable-rpc '
        f'--disable-ipv6 '
        f'--check-certificate=false '
        f'--max-connection-per-server=10 '
        f'--rpc-max-request-size=1024M '
        f'--min-split-size=10M '
        f'--allow-overwrite=true '
        f'--bt-max-peers=0 '
        f'--seed-time=0.01 '
        f'--follow-torrent=mem '
        f'--split=10 '
        f'--max-overall-upload-limit=1K '
        f'--bt-tracker=$(cat {trackerslistName}) '
        f'--max-overall-download-limit={os.environ["MAX_DOWNLOAD_SPEED"]} '
        f'--max-concurrent-downloads={os.environ["MAX_CONCURRENT_DOWNLOADS"]} '
        f'--log="{os.getcwd() + "/" + ariaLogName}"' '\n'
    )
    open(ariaScriptName, 'w').write(dat)
    if open(ariaScriptName, 'r').read() == dat:
        LOGGER.debug(subprocess.run(['chmod', '+x', ariaScriptName, '-v'],
                                    stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', ''))
        ariaDaemon = subprocess.Popen(f'./{ariaScriptName}')
        LOGGER.info(f"{ariaScriptName} started (pid {ariaDaemon.pid})")
        return
    else:
        exit(1)


def netrc():
    dot_netrc = '/root/.netrc'
    if os.path.exists('netrc'):
        if os.path.exists(dot_netrc):
            os.remove(dot_netrc)
        LOGGER.debug(subprocess.run(['cp', 'netrc', dot_netrc, '-v'],
                                    stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', ''))
        LOGGER.debug(subprocess.run(['chmod', '600', dot_netrc, '-v'],
                                    stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', ''))
    else:
        LOGGER.info("File Not Found: 'netrc'...\n'netrc' Support Disabled!")


def killAll():
    global ariaDaemon
    ariaDaemon.terminate()
    LOGGER.info(f"aria.sh killed (pid {ariaDaemon.pid})")
    LOGGER.info(subprocess.run(['pkill', 'aria2c', '-e'],
                               stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', ''))


def dl(url: str, fileName):
    DL_WAIT_TIME = int(os.environ['DL_WAIT_TIME'])
    subprocess.run(['aria2c', url, '--quiet=true', '--out=' + fileName, '--check-certificate=false'])
    time_lapsed = 0
    while time_lapsed != DL_WAIT_TIME:
        if os.path.exists(fileName):
            break
        else:
            time.sleep(0.1)
            time_lapsed += 0.1
