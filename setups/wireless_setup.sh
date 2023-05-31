#! /bin/bash

BASE_CONFIG_DIR=/etc/config

echo "Script de setup para la configuracion de Wi-Fi"
echo "Requisitos:"
echo -e "\t- Interfaz inalambrica conectada y nombrada 'wlan0'"
echo -e "\t- Interfaz inalambrica con soporte para modo AP"
echo -e "\t- Una red local con nombre 'lan' en el archivo /etc/config/network"

echo "Levantando interfaz inalambrica"
# ifconfig wlan0 up

echo "Agregando configuracion al archivo /etc/config/wireless"
echo -e '\n' >> $BASE_CONFIG_DIR/wireless
echo -e "config wifi-iface 'pvpn'" >> $BASE_CONFIG_DIR/wireless
echo -e "\toption device 'radio0'" >> $BASE_CONFIG_DIR/wireless
echo -e "\toption mode 'ap'" >> $BASE_CONFIG_DIR/wireless
echo -e "\toption ssid 'OpenWrt'" >> $BASE_CONFIG_DIR/wireless
echo -e "\toption encryption 'psk2'" >> $BASE_CONFIG_DIR/wireless
echo -e "\toption key 'test0001'" >> $BASE_CONFIG_DIR/wireless
echo -e "\toption network 'lan'" >> $BASE_CONFIG_DIR/wireless

