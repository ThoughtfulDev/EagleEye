![Python 3.5](https://img.shields.io/badge/Python-3.6%2B-blue.svg)
![OS Linux](https://img.shields.io/badge/Supported%20OS-Linux-yellow.svg)
![Lets stalk](https://img.shields.io/badge/Stalkermode-Activated-red.svg)
```
███████╗ █████╗  ██████╗ ██╗     ███████╗       ███████╗██╗   ██╗███████╗
██╔════╝██╔══██╗██╔════╝ ██║     ██╔════╝       ██╔════╝╚██╗ ██╔╝██╔════╝
█████╗  ███████║██║  ███╗██║     █████╗ Version █████╗   ╚████╔╝ █████╗  
██╔══╝  ██╔══██║██║   ██║██║     ██╔══╝   0.2   ██╔══╝    ╚██╔╝  ██╔══╝  
███████╗██║  ██║╚██████╔╝███████╗███████╗       ███████╗   ██║   ███████╗
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝       ╚══════╝   ╚═╝   ╚══════╝
                thoughtfuldev, you have been activated                                                                   
    
usage: eagle-eye.py [-h] [-sFB] [-sY] [-d] [-n [NAME]] [-json [JSON]]
                    [-fbList [FACEBOOKLIST]]

optional arguments:
  -h, --help            show this help message and exit
  -sFB, --skipfb        Skips the Facebook Search
  -sY, --skipyandex     Skips the Yandex Reverse Search
  -d, --docker          Set this flag if run in docker mode
  -n [NAME], --name [NAME]
                        Specify the persons name. Only active with the
                        --docker flag
  -json [JSON], --json [JSON]
                        Generates a json report. Specify a Filename
  -fbList [FACEBOOKLIST], --facebookList [FACEBOOKLIST]
                        A file which contains Links to Facebook Profiles. '--
                        skipfb' options must be enabled to use this
```

**This only works if their Facebook Profile is public.**

## What does this do?
You have at least one image of the person you are looking for and a clue about their name. You enter this data into EagleEye and it tries to find Instagram, Youtube, Facebook, and Twitter Profiles of this person.

## Screenshots?
[Example Report](https://github.com/ThoughtfulDev/EagleEye/blob/master/Example.pdf) (Used one Image of Emeraude Toubia)

![1](https://thoughtful-dev.com/projects/eagle-eye/1.png)  
![2](https://thoughtful-dev.com/projects/eagle-eye/2.png)  
![3](https://thoughtful-dev.com/projects/eagle-eye/3.png)            


## How does it work?
You give EagleEye a name and at least one photo. It searches this name in Facebook and performs Facial Recognition to find the right Facebook Profile.
Afterwards it uses Google and ImageRaider Reverse Image Search to find other Social Media Profiles.

If an Instagram Profile was found it will be verified by comparing a provided photo of the person to some of Instagram Pictures.

In the end you get a PDF Report. :)

## How to use it

### Docker (Preferred)
**Make sure that you have docker installed**
**Make sure that you use a LINUX distribution as the host**
1. Clone the Repository

   ``` $ git clone https://github.com/ThoughtfulDev/EagleEye ```
2. ```
   $ cd EagleEye
   $ sudo docker build -t eagle-eye - < dockerfile
   ```
3. Now create a `known` folder and a `result` folder anywhere on your PC.
4. Put the images of the known person in the known folder.
5. Change the name of the person your are searching for in `entry.sh`
6. Start the container. **Make sure to edit the paths**:
```
sudo docker run -t --net=host --env="DISPLAY" \
                           --volume="$HOME/.Xauthority:/root/.Xauthority:rw"  \
                           -v  /path/to/known:/EagleEye/known \
                           -v  /path/to/result:/result \
                           -v /path/to/EagleEye/Repository/entry.sh:/entry.sh \
                           eagle-eye

```

The result should now be in `/path/to/result`

### Automated Prequisites Installation (If Docker doesn't work)
```
wget https://raw.githubusercontent.com/ThoughtfulDev/EagleEye/master/install.sh && chmod +x install.sh && ./install.sh
```

### Manual Prequisites Installation (If you are hardcore)

For **Debian** based Distros
```
$ sudo apt update && sudo apt upgrade -y
$ sudo apt install git python3 python3-pip python3-dev
$ sudo apt install libgtk-3-dev libboost-all-dev build-essential cmake libffi-dev
$ git clone https://github.com/ThoughtfulDev/EagleEye
$ cd EagleEye && sudo pip3 install -r requirements.txt
$ sudo pip3 install --upgrade beautifulsoup4 html5lib spry
```

For **Arch**
```
$ sudo pacman -Syu
$ sudo pacman -S git python python-pip gtk3 boost cmake libffi
$ git clone https://github.com/ThoughtfulDev/EagleEye
$ cd EagleEye && sudo pip3 install -r requirements.txt
$ sudo pip3 install --upgrade beautifulsoup4 html5lib spry
```

### Firefox installation

Regardless of which option you choose make sure that you have Firefox installed.

If you are running a desktop version of Debian or Arch you likely have this installed already.

If you are not running a desktop version you may need to manually install.

### Geckodriver

Once Firefox is installed, download the [latest release](https://github.com/mozilla/geckodriver/releases/latest) of the Geckodriver for you Architecture.

**If you get a `broken pipe` Error use Geckodriver Version 0.19.1.**

**Note: If you are using Firefox ESR (like Kali does) please use the Geckodriver Version 0.17.**

Make the Geckodriver executable:
```
$ chmod +x /path/to/geckodriver
```

Note: The `geckodriver` prefers to be in your path so wherever you do set it up you will likely need to setup a link to somewhere in your PATH (or add it to your PATH).

Example:
```
$ sudo ln -s /path/to/geckodriver /usr/local/bin/geckodriver
```

### Configuration: General

Next change the value in `config.json` to the path of the `geckodriver` e.g
```
{
    "DEFAULTS": {
        ...
    },
    "WEBDRIVER": {
        "ENGINE": "firefox",
        "PATH": "/usr/local/bin/geckodriver"
    },
    "FILTER": [
        ....
    ],
    ...
}
```

### Configuration: Images

Next put at least one Image of the Person you want to find in the `known` folder.

Supported Filetypes are: **jpg/JPG, jpeg/JPEG, png/PNG, and bmp/BMP.**

## Run

Then run the program ;)
```
$ python3 eagle-eye.py
```

To see a list of all available Options just type
```
$ python3 eagle-eye.py -h
```

*The ImageRaider Reverse Image Search can take some minutes 1-15 Minutes depending on the count of Images*

## TODO

* Implement the Chrome Webdriver

## Contributing
You can always open a Pull Request

OR

[![Buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/supergirl)

## Publications/Mentions
[Eagle Eye: Search engine for Facebook, Instagram, Twitter](https://www.rebvn.com/2018/09/eagle-eye-cong-cu-tim-kiem-tai-khoan-mang-xa-hoi.html)(In Vietnamese)


## License
```
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2018 ThoughtfulDev

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  1. You just DO WHAT THE FUCK YOU WANT TO.
```
