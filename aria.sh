export MAX_DOWNLOAD_SPEED=0
export MAX_CONCURRENT_DOWNLOADS=3
TRACKER_LIST=$(curl -Ns https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt | awk '$1' | tr '\n' ',')
aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800 --check-certificate=false\
   --max-connection-per-server=10 --rpc-max-request-size=1024M \
   --bt-tracker="[$TRACKER_LIST]" --bt-max-peers=0 --seed-time=0.01 --min-split-size=10M \
   --follow-torrent=mem --split=10 \
   --daemon=true --allow-overwrite=true --max-overall-download-limit=$MAX_DOWNLOAD_SPEED \
   --max-overall-upload-limit=1K --max-concurrent-downloads=$MAX_CONCURRENT_DOWNLOADS
