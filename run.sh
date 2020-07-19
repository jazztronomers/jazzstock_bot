export INSTANCE_ID=$1
export PYTHONPATH="/workspace/jazzstock_bot:$PYTHONPATH"
DATE=$(date '+%Y%m%d')
cd /workspace/jazzstock_bot
git checkout -- .


git pull origin master
python3 -u /workspace/jazzstock_bot/main/main_crawlnaver_run.py $INSTANCE_ID >> debug_$INSTANCE_ID_$DATE.log &

