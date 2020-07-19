export INSTANCE_ID=$1
<<<<<<< HEAD
=======
export CNT=$2
>>>>>>> 3d697077266c1beaf6a54438834dc3937f3b0cef
export PYTHONPATH="/workspace/jazzstock_bot:$PYTHONPATH"
cd /workspace/jazzstock_bot
git checkout -- .


git pull origin master
<<<<<<< HEAD
python3 -u /workspace/jazzstock_bot/main/main_crawlnaver_run.py $INSTANCE_ID >> debug_$INSTANCE_ID_.log &
=======
python3 -u /workspace/jazzstock_bot/main/main_crawlnaver_run.py $INSTANCE_ID >> debug.log &
>>>>>>> 3d697077266c1beaf6a54438834dc3937f3b0cef
