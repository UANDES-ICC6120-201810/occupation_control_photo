#!/bin/bash

source_folder=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
directory="/usr/local/bin/occupation_module"

# Setup for stop bus occupation module of ZAPO proyect
echo Installing module dependencies...
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install python python-pip || echo "Python installation Failed" exit
sudo pip install virtualenv || echo "python virtualenv installation failed" exit
echo Requirements installed successfuly

echo Creting required folders ...
sudo mkdir $directory
cd $directory
echo installing python dependencies ...
sudo virtualenv env
. env/bin/activate
sudo pip install numpy || echo "Failed to install numpy" exit
sudo pip install boto3 || echo "Failed to install boto3" exit
sudo apt-get install python-opencv || echo "Failed to install OpenCV for python"
echo Copying files to folder ...
sudo cp $source_folder/run.sh $directory/run.sh
sudo cp $source_folder/main.py $directory/main.py
echo creating registers.log ...
sudo touch registers.log
echo Creating images folder ...
sudo mkdir img_folder
echo required folders and files created

echo Setting cron job default every 5 minutes
sudo crontab -l | sed "/run.sh/ c*/5 * * * * sudo sh $directory/run.sh > $directory/registers.log 2>&1" | sudo crontab -
sudo service cron reload
sudo service cron restart
echo Jos setted up correctly
