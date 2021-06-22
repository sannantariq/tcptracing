#!/bin/bash

DST=$1
INPUT_FILE_PATH=$2
OUTPUT_FILE_PATH=$3

cleanup ()
{
    relevant_text=$(cat $INPUT_FILE_PATH |   sed -e ':a; /<->$/ { N; s/<->\n//; ba; }' | grep "tcpESTAB"  |  grep "unacked")
	# get timestamp
    # echo $relevant_text
	ts=$(echo "$relevant_text" | awk '{print $1}')

	# get sender
	sender=$(echo "$relevant_text" | awk '{print $5}')

    # get receiver
    recvr=$(echo "$relevant_text" | awk '{print $6}')


	# retransmissions - current, total
    ret_current=$(echo "$relevant_text" |  grep -oP '\bretrans:.*\brcv_space'  | awk -F '[:/ ]' '{print $2}')
	ret_total=$(echo "$relevant_text" |  grep -oP '\bretrans:.*\brcv_space'  | awk -F '[:/ ]' '{print $3}')


	# get cwnd, ssthresh
	cwn=$(echo "$relevant_text" | grep -oP '\bcwnd:.*(\s|$)\bbytes_acked' | awk -F '[: ]' '{print $2}')
    ssthresh=$(echo "$relevant_text" | grep -oP '\bcwnd:.*(\s|$)\bbytes_acked' | awk -F '[: ]' '{print $4}')

	# get rtt
	rtt=$(echo "$relevant_text" |  grep -oP '\brtt:.*\/'  | awk -F '[:/ ]' '{print $2}')

	# get minrtt
	minrtt=$(echo "$relevant_text" |  grep -oP '\bminrtt:.*(\s|$)'  | awk -F '[: ]' '{print $2}')

    # get data packets out
    data_segs_out=$(echo "$relevant_text" |  grep -oP '\bdata_segs_out:.*(\s|$)'  | awk -F '[: ]' '{print $2}')

    # get_cc_algo
    cc=$(echo "$relevant_text" |  grep -oP '(\bcubic|\breno|\bbbr|\bvegas)' | awk '{print $1}')

	# concatenate into one CSV
	paste -d ',' <(printf %s "$ts") <(printf %s "$sender") <(printf %s "$recvr") <(printf %s "$ret_current") <(printf %s "$ret_total") <(printf %s "$cwn") <(printf %s "$ssthresh") <(printf %s "$rtt") <(printf %s "$minrtt") <(printf %s "$data_segs_out") <(printf %s "$cc") > $OUTPUT_FILE_PATH

	exit 0
}

trap cleanup SIGINT SIGTERM

while [ 1 ]; do 
	ss --no-header -ein dst $DST | ts '%.s' | tee -a $INPUT_FILE_PATH
done
