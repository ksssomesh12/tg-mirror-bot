# Description:

A Telegram Bot written in Python language to mirror files on the internet to Google Drive

# Credits:

- This repository is a fork-clone of the following repositories.

  > [lzzy12's python-aria-mirror-bot](https://github.com/lzzy12/python-aria-mirror-bot)

  > [afdulfauzan's python-aria-mirror-bot](https://github.com/afdulfauzan/python-aria-mirror-bot)

  > [magneto261290's magneto-python-aria](https://github.com/magneto261290/magneto-python-aria)

    All credits goes to the maintainers of the above repositories.


- Few useful additional features have been implemented on top of them.
- This repository utilises trackers for torrent/magnet downloads from [Trackerslist Website](https://trackerslist.com).

# Supported Features:

## From Source Repos

- Mirror Torrents
- Mirror Direct Links
- Mirror Telegram Files
- Upload Files after Archiving/Unarchiving
- Download and Upload Progress, Speeds and ETAs
- Docker Support
- Uploading To Team Drives
- Index Link Support
- Shortener Support
- Service Account Support
- Mirror 'youtube-dl' Supported Links
- Mirror Files on MEGA.NZ (Not Very Stable)

## Additional Features

- Dynamic Config Support, to facilitate easier and streamlined experience for editing config files.
- Sync Config Files at every /restart command.
- Edit values of environment variables in 'config.env' from within the bot using InlineKeyboardButtons.
- 'aria2c' daemon starts as a subprocess from within the 'bot' python module, facilitating better handling of processes. This also results in both 'aria2c' daemon and the 'bot' python module restarting with every '/restart' command.
- Support for using custom tracker list formatted as a text file, as required by 'aria2c' daemon.

## Supported Archive File Types
```
ZIP RAR TAR 7Z ISO WIM CAB GZIP BZIP2 APM ARJ CHM CPIO CramFS DEB DMG FAT HFS LZH LZMA LZMA2 MBR MSI MSLZ NSIS NTFS RPM SquashFS UDF VHD XAR Z
```

# Development Status:

## To-Dos

- Add option to select files for torrent/magnet downloads.

**NOTE:** All the above to-dos are aimed at achieving zero human-intervention after initial deploy to Heroku.

## Info of Branches

- **master** : most stable environment for production deploys.
- **staging** : testing new features, fixes or better implementations of already existing ones.
- **dev** : major feature updates that are under development - currently, added support for 'mega-dl'.

# Deploying:

## Prerequisites

- Install Python3.
```
sudo apt install python3
```

## Cloning and Setting Up Config File

- Download and Extract the [Latest Release Package](https://github.com/ksssomesh12/tg-mirror-bot/releases):
```
mkdir ~/Downloads/deploy_heroku
mv ~/Downloads/deploy_release_v* ~/Downloads/deploy_heroku
cd ~/Downloads/deploy_heroku
tar xzvf deploy_release_v*
rm -v deploy_release_v*
```

- Copy and Edit the Config file:
```
cp config_sample.env config.env
nano config.env
```

- Remove the first line saying:
```
_____REMOVE_THIS_LINE_____=True
```

Fill up rest of the fields. The description of each field is given below.

### Required Fields

- **BOT_TOKEN** : The telegram bot token that you get from [@BotFather](https://t.me/botfather).
- **GDRIVE_FOLDER_ID** : This is the folder ID of the Google Drive folder to which you want to upload all the mirrors.
- **DOWNLOAD_DIR** : The path to the folder where the downloads will be downloaded locally, before uploading to Google Drive.
- **OWNER_ID** : The Telegram user ID (not username) of the owner of the bot.
- **DOWNLOAD_STATUS_UPDATE_INTERVAL** : A short interval of time in seconds after which the Mirror progress message is updated (5 seconds at least).
- **AUTO_DELETE_MESSAGE_DURATION** : Interval of time (in seconds), after which the bot deletes its message (and command message) which is expected to be viewed instantly (set to '-1' to never automatically delete messages).
- **TELEGRAM_API** : This is to authenticate to your telegram account for downloading Telegram files. You can get this from [here](https://my.telegram.org).
- **TELEGRAM_HASH** : This is to authenticate to your telegram account for downloading Telegram files. You can get this from [here](https://my.telegram.org).
- **MAX_DOWNLOAD_SPEED** : Set the maximum download speed. By default, it is set to '0' (unlimited).
- **MAX_CONCURRENT_DOWNLOADS** : Set the maximum concurrent downloads. By default, it is set to '3'.
- **TRACKERSLIST** : Set the URL of the trackerslist text file. By default, it is set to 'https://trackerslist.com/all_aria2.txt'.
- **USE_TELEGRAPH** : Set to "true" to use Telegra.ph for search results from '/list' bot command, or else set to "false".

**NOTE:** The trackerslist text file must contain tracker URLs in a single line, separated by commas, as required by 'aria2c'.

### Optional Fields (leave empty if unsure)

- **IS_TEAM_DRIVE** : Set to "true" if GDRIVE_FOLDER_ID is from a Team Drive, or else set to "false" or leave it empty.
- **USE_SERVICE_ACCOUNTS** : Whether to use service accounts or not. For this to work see  "Using service accounts" section below.
- **STOP_DUPLICATE_MIRROR** : Set this to "true", if you want to check for duplicate files (using file name, and not file hash) in Google Drive matching the requested download and stop the download if found any.
- **ENABLE_MEGA_SUPPORT**: Set this to "false", if you want to disable downloading of MEGA.NZ files.
- **MEGA_API_KEY**: API Key of your MEGA.NZ account. Get it from [MEGA SDK Page](https://mega.nz/sdk).
- **MEGA_EMAIL_ID**: Email ID of your MEGA.NZ account.
- **MEGA_PASSWORD**: Password of your MEGA.NZ account.
- **INDEX_URL** : Refer to [GDIndex repo](https://github.com/maple3142/GDIndex/). The URL should not have any trailing '/'.
- **SHORTENER** : URL of the Shortener.
- **SHORTENER_API** : API Key of the Shortener.

        Supported Shorteners:
        
        > exe.io
        > gplinks.io
        > shrinkme.io
        > urlshortx.com
        > shortzon.com
        
        Additionally, some other shorteners are also supported unofficially.

## Getting Google OAuth API Credential File

- Visit the [Google Cloud Console](https://console.developers.google.com/apis/credentials).
- Go to the OAuth Consent tab, fill it, and save.
- Go to the Credentials tab and click Create Credentials -> OAuth Client ID.
- Choose Other and Create.
- Use the download button to download your credentials.
- Move the downloaded file to the 'deploy_heroku' folder, and rename it to 'credentials.json'.
- Visit [Google API Library](https://console.developers.google.com/apis/library).
- Search for Drive and enable it if it is disabled.

## Setup

- Install Requirements:
```
pip3 install -r requirements.txt
```
- Use 'pipenv' for better compatibility (optional):
```
pipenv install -r requirements.txt
pipenv shell
```
- Run 'setup.py', and authorize the AppFlow to generate 'token.pickle':
```
python3 setup.py
```
- Enter the appropriate choice in the input prompt, to use static/dynamic config.

  In case of static config, the setup is complete here.

  In case of dynamic config, continue to the next section.

### Dynamic Config (optional)

- If you are running this setup script for the first time, enter the appropriate choice in the input prompt and continue to the next step.
- Create a new folder in your personal Google Drive, irrespective of the folder you use for uploading files with this bot (no constraints at all).
- Change the permissions of this newly created folder to 'Anyone on the Internet with this link can view'.
- Enter the FolderId of the newly created folder in the input prompt, and continue with the setup.
- For 'DL_WAIT_TIME' reference, see below:

    > **DL_WAIT_TIME** : Time to wait for aria2c to download the config files. By default it's set to '5' seconds, which is more than enough for deploying the bot to Heroku. If 'DL_WAIT_TIME' lapses, and the config files are not downloaded due to any reason, the bot exits with exit code (1).

- The config files will be uploaded to Google Drive, and then deleted, except for 'dynamic.env'.
- The setup script will exit with 'Setup Completed' message.
- Now, the docker image can be deployed with 'dynamic.env' file.

**NOTE:** If you have already run this setup script and want to update the existing config files in drive, enter the appropriate choice in the input prompt. In the next step, enter the FileId of the existing 'dynamic.env' in the input prompt, and the updated files will be uploaded to Google Drive. Now, you can choose to keep the old config files or delete them.

# Deploy to Heroku:

## Creating a Heroku App

- Create a [free Heroku Account](https://id.heroku.com/signup/login).
- Install Heroku CLI:
```
sudo snap install --classic heroku
```
- Login into your Heroku Account:
```
heroku login
```
- Visit [Heroku Dashboard](https://dashboard.heroku.com) and create a new app with any name (for our reference, your-mirror-bot) and with any region you prefer, for your app to be served from.
- In the Deploy tab of your app dashboard, select  'Heroku Git' in Deployment Method.
- Change the Stack for the App using Heroku CLI:
```
heroku stack:set container --app your-mirror-bot
```
- Initialise the project files as a Git Repository, push the Repo to 'Heroku Git' and build the Docker Image:
```
cd ~/Downloads/deploy_heroku
git init
git add .
git commit -m "initial commit"
heroku git:remote --app your-mirror-bot
git push heroku master
```
- If the Docker Image Build succeeds, then, your push to the remote repository will succeed, otherwise, your push to the remote repository is rejected as the Docker Image Build fails.

## Run/Terminate the App

You can run/terminate the app by allocating/deallocating dynos to the app.

### Using Dashboard

- In the app dashboard, under resources tab, use the 'Edit Dyno Formation' button in Dynos section to change the working state of the app.

### Using CLI

- To Run:
```
heroku ps:scale worker=1 --app your-mirror-bot
```
- To Terminate:
```
heroku ps:scale worker=0 --app your-mirror-bot
```
- To Check Status:
```
heroku ps --app your-mirror-bot
```
- To Tail App Logs:
```
heroku logs --tail --app your-mirror-bot
```

# Bot Commands:

- **start** - Start the bot
- **mirror** - Mirror the provided link to Google Drive
- **unzipmirror** - Mirror the provided link and if the file is in archive format, it is extracted and then uploaded to Google Drive
- **tarmirror** - Mirror the provided link and upload in archive format (.tar) to Google Drive
- **cancel** - Reply with this command to the source message, and the download will be cancelled
- **cancelall** - Cancels all running tasks (downloads, uploads, archiving, unarchiving)
- **list** - Searches the Google Drive folder for any matches with the search term and presents the search results in a Telegraph page
- **status** - Shows the status of all downloads and uploads in progress
- **authorize** - Authorize a group chat or, a specific user to use the bot
- **unauthorize** - Unauthorize a group chat or, a specific user to use the bot
- **ping** - Ping the bot
- **restart** - Restart the bot
- **stats** - Shows the stats of the machine that the bot is hosted on
- **help** - To get the help message
- **log** - Sends the log file of the bot and the log file of 'aria2c' daemon (can be used to analyse crash reports, if any)
- **clone** - Clone folders in Google Drive (owned by someone else) to your Google Drive 
- **watch** - Mirror through 'youtube-dl' to Google Drive
- **tarwatch** - Mirror through 'youtube-dl' and upload in archive format (.tar) to Google Drive
- **delete** - Delete files in Google Drive matching the given string
- **config** - Edit 'config.env' file

**NOTE:** The above listed command descriptions can be copied and pasted in 'edit bot commands' section, when editing the bot settings with [@BotFather](https://t.me/botfather).
