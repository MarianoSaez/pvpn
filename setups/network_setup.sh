#! /bin/bash

BASE_CONFIG_DIR=/etc/config
CONFIG_FILE=network

echo "Script de setup para la configuracion de la LAN privada"
echo "Requisitos: N/A"

echo "Agregando configuracion al archivo /etc/config/network"
echo -e '\n' >> $BASE_CONFIG_DIR/$CONFIG_FILE
echo -e "config interface 'lan'" >> $BASE_CONFIG_DIR/$CONFIG_FILE
echo -e "\toption ifname 'wlan0'" >> $BASE_CONFIG_DIR/$CONFIG_FILE
echo -e "\toption ipaddr '10.0.0.1'" >> $BASE_CONFIG_DIR/$CONFIG_FILE
echo -e "\toption netmask '255.255.255.0'" >> $BASE_CONFIG_DIR/$CONFIG_FILE
echo -e "\toption proto 'static'" >> $BASE_CONFIG_DIR/$CONFIG_FILE

