#!/bin/bash

url=$1
curl "$url" |  sed 's|</b>|-|g' | sed 's|<[^>]*>||g' > /tmp/stripped

machine=$(cat /tmp/stripped | grep hostname | tr -s ' ' |  cut -d" " -f3)
port=$(cat /tmp/stripped | grep debug | tr -s ' ' |  cut -d" " -f3)

cmd="ssh -f  $machine  -L 5005:$machine:$port -N"
echo $cmd
$cmd


