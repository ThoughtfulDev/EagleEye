![Python 3.5](https://img.shields.io/badge/Python-3.6%2B-blue.svg)
![OS Linux](https://img.shields.io/badge/Supported%20OS-Linux-yellow.svg)
![Lets stalk](https://img.shields.io/badge/Stalkermode-Activated-red.svg)
```
███████╗ █████╗  ██████╗ ██╗     ███████╗   ███████╗██╗   ██╗███████╗
██╔════╝██╔══██╗██╔════╝ ██║     ██╔════╝   ██╔════╝╚██╗ ██╔╝██╔════╝
█████╗  ███████║██║  ███╗██║     █████╗     █████╗   ╚████╔╝ █████╗  
██╔══╝  ██╔══██║██║   ██║██║     ██╔══╝     ██╔══╝    ╚██╔╝  ██╔══╝  
███████╗██║  ██║╚██████╔╝███████╗███████╗   ███████╗   ██║   ███████╗
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚══════╝   ╚═╝   ╚══════╝
                    Jerry Shaw, you have been activated    

Find your friends Social Media Profiles with ease     
```

**This only works if their Facebook Profile is public**

## What does this do?
In simple words you have at least one Image of the Person you are looking for and a clue about its name. You feed this program with it and it tries to find Instagram, Youtube, Facebook, Twitter Profiles of this Person.

## How does it work?
You give it a name and at least one photo. It then searches Facebook for this name and does Facial Recognition to determine the right Facebook Profile.
After that it does a Google and ImageRaider Reverse Image Search to find other Social Media Profiles.

If a Instagram Profile was found it will be verified by comparing your known photo of the Person to some of the Instagram Pictures.

In the end you get a PDF Report :)

## How to use it

### Automated Prequisites Installation
```
wget https://raw.githubusercontent.com/ThoughtfulDev/EagleEye/master/pre.sh && chmod +x pre.sh && ./pre.sh
```

### Manual Prequisites Installation
```
$ sudo apt update && sudo apt upgrade -y
$ sudo apt install git python3 python3-pip python3-dev
$ sudo apt install libgtk-3-dev libboost-all-dev build-essential cmake libffi-dev
$ git clone https://github.com/ThoughtfulDev/EagleEye
$ cd EagleEye && sudo pip3 install -r requirements.txt
$ sudo pip3 install --upgrade beautifulsoup4 html5lib spry
```

Regardless of which option you choose make sure that you have Firefox installed
If you have Firefox installed, download the [latest release](https://github.com/mozilla/geckodriver/releases/latest) of the Geckodriver for you Architecture.
**If you get a `broken pipe` Error use Geckodriver Version 0.19.1**

**Note: If you are using Firefox ESR(like Kali does) please use the Geckodriver Version 17**

Next change the value in `config.json` to the path of the geckodriver e.g
```
{
    "DEFAULTS": {
        ...
    },
    "WEBDRIVER": {
        "ENGINE": "firefox",
        "PATH": "PATH TO geckodriver e.g C:\\Program Files\\geckodriver.exe"
    },
    "FILTER": [
        ....
    ],
    ...
}
```

Make the Geckodriver executable
```
$ chmod +x /path/to/geckodriver
```

*I will try to implement the Chrome Webdriver as soon as possible*

Next put at least one Image of the Person you want to find in the `known` folder.
(**Has to be .jpg for now**)

Then run the program ;)
```
$ python3 eagle-eye.py
```

To see a list of all available Options just type
```
$ python3 eagle-eye.py -h
```

*The ImageRaider Reverse Image Search can take some minutes 1-15 Minutes depending on the count of Images*


## Screenshots?
[Example Report](https://github.com/ThoughtfulDev/EagleEye/blob/master/Example.pdf) (Used one Image of Emeraude Toubia)

![1](https://thoughtful-dev.com/projects/eagle-eye/1.png)  
![2](https://thoughtful-dev.com/projects/eagle-eye/2.png)  
![3](https://thoughtful-dev.com/projects/eagle-eye/3.png)            

## Contributing
You can always open a Pull Request

OR

[![Buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/supergirl)


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

  0. You just DO WHAT THE FUCK YOU WANT TO.
```
