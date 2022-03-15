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

debian_install() {
    sudo apt update && sudo apt upgrade -y
    sudo apt install git python3 python3-pip python3-dev
    sudo apt install libgtk-3-dev libboost-all-dev build-essential cmake libffi-dev
}

arch_install_package() {
    package=$1
    if sudo pacman -Qi $package > /dev/null ; then
        echo "$package is already installed"
    else
        echo "Installing $package"
        sudo pacman -S $package
    fi
}

arch_install() {
    sudo pacman -Syu
    arch_install_package "git"
    arch_install_package "python"
    arch_install_package "python-pip"
    arch_install_package "gtk3"
    arch_install_package "boost"
    arch_install_package "cmake"
    arch_install_package "libffi"
}

fedora_install() {
    sudo yum update
}

python_setup() {
    git clone https://github.com/ThoughtfulDev/EagleEye
    cd EagleEye && sudo pip3 install -r requirements.txt
    python3 -m pip install --user --upgrade beautifulsoup4 html5lib spry

    echo  "Installation done"
    echo "Now download the Geckodriver"
}

if [ "$(grep -Ei 'debian|ubuntu|mint' /etc/*release)" ]; then
    debian_install
    python_setup
fi

if [ "$(grep -Ei 'arch' /etc/*release)" ]; then
    arch_install
    python_setup
fi

if [ "$(grep -Ei 'fedora|redhat' /etc/*release)" ]; then
    echo "yum is currently not supported."
fi


