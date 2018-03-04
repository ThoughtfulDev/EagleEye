#!/bin/bash

echo "
███████╗ █████╗  ██████╗ ██╗     ███████╗       ███████╗██╗   ██╗███████╗
██╔════╝██╔══██╗██╔════╝ ██║     ██╔════╝       ██╔════╝╚██╗ ██╔╝██╔════╝
█████╗  ███████║██║  ███╗██║     █████╗         █████╗   ╚████╔╝ █████╗  
██╔══╝  ██╔══██║██║   ██║██║     ██╔══╝         ██╔══╝    ╚██╔╝  ██╔══╝  
███████╗██║  ██║╚██████╔╝███████╗███████╗       ███████╗   ██║   ███████╗
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝       ╚══════╝   ╚═╝   ╚══════╝
Install Script
"

sudo apt update && sudo apt upgrade -y
sudo apt install git python3 python3-pip python3-dev
sudo apt install libgtk-3-dev libboost-all-dev build-essential cmake libffi-dev
git clone https://github.com/ThoughtfulDev/EagleEye
cd EagleEye && sudo pip3 install -r requirements.txt
sudo pip3 install --upgrade beautifulsoup4 html5lib spry

echo  "Installation done"
echo "Now download the Geckodriver"