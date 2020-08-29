DATE_IDX_FROM=$1
DATE_IDX_TO=$2
CONDLIST="TA TB TC"
PARALLEL=8

PATH_ROOT="/workspace/jazzstock_bot"
# PATH_ROOT="/project/work/jobpipeline_prev/jazzstock_bot"

PATH_SRC_EACHDAILY="$PATH_ROOT/main/main_simulation_eachcode_daily.py"
PATH_SIMULATION="$PATH_ROOT/simulation/result"

NOW=$(date '+%Y%m%d%H%M%S')

echo $NOW
echo $PATH_SIMULATION


#usage: jazzstock_util_stockcode.py [-h] [--row_num_from f] [--row_num_to t] [--date_idx d] [--verbose v] [--whom w] [--window n]
#                                   [--seperator s] [--min_market_cap m] [--descending m]


for COND in TA;do
        mkdir -p $PATH_SIMULATION/$NOW/$COND
        echo $PATH_SIMULATION/$NOW/$COND
        for ((DIDX=$DATE_IDX_FROM;DIDX>=$DATE_IDX_TO;DIDX--));
        do
                STOCKCODE_NEW=`python3 $PATH_ROOT/util/jazzstock_util_stockcode.py --row_num_from 0 --row_num_to 50 --date_idx $DIDX`
                                                                # --whom for \
                                                                # --window 5 \
                                                                # --min_market_cap 1 \
                                                                # --descending DESC`
                STOCKCODE_ACC=`python3 $PATH_ROOT/util/get_stockcode_from_account.py --account_path $PATH_SIMULATION/$NOW/$COND`
                STOCKCODE_MERGED="$STOCKCODE_NEW $STOCKCODE_ACC"
                STOCKCODE_REMOVE_DUP=`echo "$STOCKCODE_MERGED" | xargs -n1 | sort -u | xargs`

		echo $DIDX
                echo $STOCKCODE_NEW
		echo $STOCKCODE_ACC
		echo $STOCKCODE_MERGED
		echo $STOCKCODE_REMOVE_DUP
	

                for EACHCODE in $STOCKCODE_REMOVE_DUP; do
                        while [ $(pgrep python3 | wc -l) -gt $PARALLEL ]
                        do
                                sleep 0.5
                        done
                        echo $EACHCODE
			python3 -u $PATH_SRC_EACHDAILY --stockcode $EACHCODE --date_idx $DIDX --purchased 0 --amount 0 --histpurchased 0 --histselled 0 --condition_label $COND --account_path "$PATH_SIMULATION/$NOW/$COND/account_<stockcode>.csv" >> $PATH_SIMULATION/$NOW/$COND/fulllog.log 2>&1 &
                        sleep 0.5

                done
        done
done
