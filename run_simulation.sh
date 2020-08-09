STOCKCOUNT=$1
PARALLEL=$2
DAYFROM=$3
GROUP=$4



STOCKCODE=`python3 /workspace/jazzstock_bot/test/get_stockcode_for_simulation.py $STOCKCOUNT $GROUP`
NOW=$(date +%s)
PATH_OUTPUT="/workspace/jazzstock_bot/log/simulation_$NOW"



for CONDITION_LABEL in TA TB TC TP ; do
	mkdir -p $PATH_OUTPUT/$CONDITION_LABEL
	for EACHCODE in $STOCKCODE; do
		while [ $(pgrep python3 | wc -l) -gt $PARALLEL ]
		do
			sleep 0.5
		done 
		## echo DO.... $CONDITION_LABEL $EACHCODE
		python3 -u /workspace/jazzstock_bot/crawl/jazzstock_core_simulation.py $EACHCODE $DAYFROM $CONDITION_LABEL > $PATH_OUTPUT/$CONDITION_LABEL/$EACHCODE.log &
		sleep 0.5
	done


	python3 /workspace/jazzstock_bot/log/logparser_account.py $CONDITION_LABEL $NOW
done


