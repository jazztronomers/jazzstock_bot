INSTANCE_ID=$1
WINDOW=$2
CNT=$3

export PYTHONPATH="/workspace/jazzstock_bot:$PYTHONPATH"
python3 /workspace/jazzstock_bot/main/main_crawlnaver_run.py $INSTANCE_ID $WINDOW $CNT
