INSTANCE_ID=$1
WINDOW=$2
CNT=$3

export PYTHONPATH="/workspace/jazzstock_bot:$PYTHONPATH"
cd /workspace/jazzstock_bot
git pull origin master
python3 -u /workspace/jazzstock_bot/main/main_crawlnaver_run.py $INSTANCE_ID $WINDOW $CNT >> debug.log &
