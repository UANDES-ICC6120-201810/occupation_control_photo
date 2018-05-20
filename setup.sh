#!/bin/bash
parent_folder=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

# Setup for stop bus occupation module of ZAPO proyect

echo Installing module dependencies...
sudo apt-get install python python-pip || echo "Installation Failed" exit
sudo pip install numpy || echo "Python requirements could not be installed" exit
sudo apt-get install python-opencv || echo "OpeCv for python could not be installed" exit
echo Requirements installed successfuly

echo Creting required folders and files
cd "$parent_folder"
touch registers.log
mkdir ../img_folder
echo required folders and files created

echo Setting cron job default every 5 minutes
(sudo crontab -l 2>/dev/null; echo "*/5 * * * * sudo sh "$parent_folder"/run.sh > "$parent_folder"/registers.log 2>&1") | sudo crontab -
sudo service cron reload
sudo service cron restart
echo Jos setted up correctly
