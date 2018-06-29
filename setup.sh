#!/bin/bash

sudo ip route del default via 192.168.1.1 dev eth0

source_folder=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
directory="/usr/local/bin/occupation_module"

# Setup for stop bus occupation module of ZAPO proyect
echo Installing module dependencies...
apt-get update && sudo apt-get -y upgrade
apt-get install python python-pip || echo "Python installation Failed" || exit
echo Requirements installed successfuly

echo Creting required folders ...
rm -rf $directory
mkdir $directory
cd $directory

echo installing python dependencies ...
pip install numpy || echo "Failed to install numpy" || exit
pip install boto3 || echo "Failed to install boto3" || exit
pip install requests || echo "Failed to install requests" exit
apt-get install python-opencv || echo "Failed to install OpenCV for python"

echo Copying files to folder ...
cp $source_folder/run.sh $directory/run.sh
cp $source_folder/main.py $directory/main.py
cp $source_folder/settings.py $directory/settings.py
cp $source_folder/crontab $directory/crontab

echo creating registers.log ...
touch registers.log

echo Creating images folder ...
mkdir img_folder
echo required folders and files created

echo Setting cron job default every 5 minutes
echo "Implementing new crontab"
crontab $directory/crontab
service cron reload
service cron restart
echo "Jos implemented correctly"
