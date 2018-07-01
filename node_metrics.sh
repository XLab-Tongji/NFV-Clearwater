#!/bin/bash

# 获取node层数据的url
# 用法: sh node_metrics.sh <timestamp1> <timestamp2>

echo "bono:"
curl "http://lab205.jios.org:12002/filedownload?hostId=10274&timeFrom=$1&timeTill=$2" --output "./data/sla/node/bono.xlsx"
echo "homestead:"
curl "http://lab205.jios.org:12002/filedownload?hostId=10280&timeFrom=$1&timeTill=$2" --output "./data/sla/node/homestead.xlsx"
echo "sprout:"
curl "http://lab205.jios.org:12002/filedownload?hostId=10305&timeFrom=$1&timeTill=$2" --output "./data/sla/node/sprout.xlsx"
echo "Done!"
