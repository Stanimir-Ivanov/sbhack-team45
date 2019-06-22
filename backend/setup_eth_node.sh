#!/bin/sh
sudo apt update
sudo apt upgrade
sudo apt-get install npm
sudo npm install -g ganache-cli
sudo npm install -g truffle
iptables -t nat -A  PREROUTING -d "public_ip" -j DNAT --to-destination "private_ip"
iptables -t nat -A POSTROUTING -s "private_ip" -j SNAT --to-source "public_ip"
ganache-cli -h "private_ip"
truffle migrate
# Then connect on public IP
