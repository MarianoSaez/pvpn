#! /bin/bash

echo "Script de configuracion de paquetes necesarios"

echo "Actualizando repositorios"
opkg update

echo "Instalando paquetes del sistema necesarios"
opkg install python3 libpam

echo "Instalando paquetes de Python necesarios"
# Obtener PIP
python ./get-pip.py

# Instalar simplepam manualmente
tar -xzvf simplepam-0.1.5.tar.gz
cd simplepam-0.1.5/
python setup.py install
cd ..

# Instalar requirements.txt
pip install -r requirements.txt


