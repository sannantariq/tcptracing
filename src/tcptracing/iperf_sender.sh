#!/usr/bin/env bash

dst=$1
port=$2
cca=$3
duration=$4
totaltime=$5

echo "dst=$dst, port=$port, cca='$cca', duration=$duration total_duration=$totaltime"
end=$((SECONDS+totaltime))
echo "end=$end"

while [ $SECONDS -lt $end ]; do 
  iperf3 -c $dst -p $port -C $cca -t $duration
done