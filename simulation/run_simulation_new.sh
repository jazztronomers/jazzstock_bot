DATE_IDX=$1
PERIOD=$2
COUNT=$3
WINDOW=$4
DESC=$5
PARALLEL=2
# 기관 100일 부터 80 까지 , 5종목씩 , 기관수급 5일 강도순으로


DATE_TO=$((DATE_IDX-$PERIOD))
echo $DATE_TO

NOW=$(date +%s)
PATH_OUTPUT="/workspace/jazzstock_bot/simulation/result_$NOW"
PATH_SIMULATION_MAIN="/workspace/jazzstock_bot/crawl/jazzstock_core_simulation.py"

# PATH_OUTPUT TEMPLATE : /workspace/jazzstock_bot/simulation/result_$NOW/<CONDNAME>/ STOCKCODE.log , ACC.csv

for ((didx=$DATE_IDX;didx>=$DATE_TO;didx--));
do
	for COND in TA; do
		mkdir -p $PATH_OUTPUT/$COND
		STOCKCODE_ACC=`python3 /workspace/jazzstock_bot/simulation/parse_account.py $PATH_OUTPUT/$COND`
		STOCKCODE_NEW=`python3 /workspace/jazzstock_bot/test/get_stockcode_for_simulation.py \
           			--whom $WINDOW \
           			--descending $DESC \
           			--row_num_to $COUNT \
           			--date_idx $didx`

		STOCKCODE_MERGE="$STOCKCODE_NEW $STOCKCODE_ACC"
		echo $didx, $STOCKCODE_MERGE
		for EACHCODE in $STOCKCODE_MERGE; do
			while [ $(pgrep python3 | wc -l) -gt $PARALLEL ]
			do
				sleep 0.5
			done
			echo $EACHCODE
			python3 -u $PATH_SIMULATION_MAIN $EACHCODE $didx $COND $PATH_OUTPUT/$COND/account.csv >> $PATH_OUTPUT/$COND/$EACHCODE.log &
			sleep 0.5

		done
	done
done
