for ec in A P; do
	mkdir -p /workspace/jazzstock_bot/log/simulation/$ec
	for es in 004770; do
		while [ $(pgrep python3 | wc -l) -gt 2 ]
		do
			sleep 0.5
		done 
		echo DO.... $ec $es
		python3 -u /workspace/jazzstock_bot/crawl/jazzstock_core_simulation.py $es 10 $ec > /workspace/jazzstock_bot/log/simulation/$ec/$es.log &
		sleep 0.5
	done
done


