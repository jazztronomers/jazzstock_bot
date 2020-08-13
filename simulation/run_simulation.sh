ㅇDATE_IDX=$1
PERIOD=$2
COUNT=$3
WINDOW=$4
DESC=$5

# 기관 100일 부터 80 까지 , 5종목씩 , 기관수급 5일 강도순으로 

NOW=$(date +%s)
PATH_OUTPUT="/workspace/jazzstock_bot/simulation/result_$NOW"
STOCKCODE=`python3 /workspace/jazzstock_bot/test/get_stockcode_for_simulation.py \
	   --whom $WINDOW \
	   --descending $DESC \
	   --row_num_to $COUNT \
	   --date_idx $DATE_IDX`

for ((didx=$DATE_IDX;didx<=$DATE_IDX+$PERIOD;i++));
do
	echo "========================================================================================"
	echo $WINDOW , $didx
	echo "========================================================================================"

	for CONDITION_LABEL in TA; do
		mkdir -p $PATH_OUTPUT/$GROUP/$CONDITION_LABEL
		for EACHCODE in $STOCKCODE; do
			while [ $(pgrep python3 | wc -l) -gt $PARALLEL ]
			do
			sleep 0.5
			done 
			
		python3 -u /workspace/jazzstock_bot/crawl/jazzstock_core_simulation.py $EACHCODE $DAYFROM $CONDITION_LABEL $PATH_OUTPUT/$GROUP/$CONDITION_LABEL/account.csv > $PATH_OUTPUT/$GROUP/$CONDITION_LABEL/$EACHCODE.log &
			sleep 0.5
	done


	python3 /workspace/jazzstock_bot/simulation/logparser_account.py $CONDITION_LABEL $GROUP $NOW
done
	

echo " "
echo " "

done
