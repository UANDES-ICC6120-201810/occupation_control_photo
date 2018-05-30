#!/bin/bash

parent_folder=$( cd "$(dirname "${BASH_SOURCE[0]}")" ;pwd -P )
cd "$parent_folder"

echo $parent_folder

sudo python main.py rtsp://192.168.1.190:554
