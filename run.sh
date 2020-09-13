export INSTANCE_ID=$1
export PYTHONPATH="/workspace/jazzstock_bot:/workspace"
DATE=$(date '+%Y%m%d')
python3 -u /workspace/jazzstock_bot/main/main_crawlnaver_run.py $INSTANCE_ID >> /workspace/jazzstock_bot/log/debug_$INSTANCE_ID_$DATE.log &

