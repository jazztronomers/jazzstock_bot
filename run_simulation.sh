STOCKCOUNT=$1
PARALLEL=$2
DAYFROM=$3



STOCKCODE=`python3 /workspace/jazzstock_bot/test/get_stockcode_for_simulation.py $STOCKCOUNT`



for CONDITION_LABEL in TP TA TB TC ; do
	mkdir -p /workspace/jazzstock_bot/log/simulation/$CONDITION_LABEL
	for EACHCODE in $STOCKCODE; do
		while [ $(pgrep python3 | wc -l) -gt $PARALLEL ]
		do
			sleep 0.5
		done 
		echo DO.... $CONDITION_LABEL $EACHCODE
		python3 -u /workspace/jazzstock_bot/crawl/jazzstock_core_simulation.py $EACHCODE $DAYFROM $CONDITION_LABEL > /workspace/jazzstock_bot/log/simulation/$CONDITION_LABEL/$EACHCODE.log &
		sleep 0.5
	done
done


