#!/bin/bash

# Paths
UPLINK="/home/lalan/Desktop/WorkingD/pwq/RN-Mahimahi/car-snaroya-smestad.up"
DOWNLINK="/home/lalan/Desktop/WorkingD/pwq/RN-Mahimahi/car-snaroya-smestad.down"

SERVER_LOG="/home/lalan/Desktop/WorkingD/pwq/Multi-client-AdHoc-RelNT-Server/Reno/Reno_3%_Throu_102.txt"
QDISC_LOG="/home/lalan/Desktop/WorkingD/pwq/Multi-client-AdHoc-RelNT-Server/Reno/Reno_3%_Throu_qdisc_102.txt"

# Run everything INSIDE Mahimahi
mm-link "$UPLINK" "$DOWNLINK" -- bash -c "

sleep 1

echo 'Starting tc configuration...'

# Step 1: Apply netem with handle
sudo tc qdisc del dev ingress root 2>/dev/null
# To apply random loss
#sudo tc qdisc add dev ingress root handle 1: tbf rate 20mbit buffer 1500 limit 10MB
#sudo tc qdisc add dev ingress parent 1:1 handle 30: netem limit 7000 delay 100ms loss random 3%

# To apply bursty loss
#sudo tc qdisc add dev ingress root handle 1: tbf rate 20mbit buffer 1500 limit 10MB
#sudo tc qdisc add dev ingress parent 1:1 handle 30: netem limit 7000 delay 100ms loss state 3 25

# To apply 100ms delay
#sudo tc qdisc add dev ingress root handle 1: tbf rate 20mbit buffer 1500 limit 10MB
#sudo tc qdisc add dev ingress parent 1:1 handle 30: netem limit 7000 delay 100ms

echo 'Starting QUIC server...'

./out/Default/quic_server   --quic_response_cache_dir=/home/lalan/Desktop/WorkingD/pwq/dash-5m --certificate_file=net/tools/quic/certs/out/leaf_cert.pem   --key_file=net/tools/quic/certs/out/leaf_cert.pkcs8 \
  >> $SERVER_LOG &

echo 'Starting qdisc logging...'

while true; do
  date >> $QDISC_LOG
  tc -s qdisc show dev ingress >> $QDISC_LOG
  sleep 1
done
"
