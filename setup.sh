#!/bin/bash

source_folder=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
directory="/usr/local/bin/occupation_module"

# Setup for stop bus occupation module of ZAPO proyect
echo Installing module dependencies...
sudo apt-get install python python-pip || echo "Installation Failed" exit
sudo pip install numpy || echo "Python requirements could not be installed" exit
sudo apt-get install python-opencv || echo "OpeCv for python could not be installed" exit
echo Requirements installed successfuly

echo Creting required folders ...
sudo mkdir $directory
cd $directory
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
