```
$$$$$$$$\                    $$\                 $$$$$$$$\                    
$$  _____|                   $$ |                $$  _____|                   
$$ |      $$$$$$\   $$$$$$\  $$ | $$$$$$\        $$ |     $$\   $$\  $$$$$$\  
$$$$$\    \____$$\ $$  __$$\ $$ |$$  __$$\       $$$$$\   $$ |  $$ |$$  __$$\ 
$$  __|   $$$$$$$ |$$ /  $$ |$$ |$$$$$$$$ |      $$  __|  $$ |  $$ |$$$$$$$$ |
$$ |     $$  __$$ |$$ |  $$ |$$ |$$   ____|      $$ |     $$ |  $$ |$$   ____|
$$$$$$$$\\$$$$$$$ |\$$$$$$$ |$$ |\$$$$$$$\       $$$$$$$$\\$$$$$$$ |\$$$$$$$\ 
\________|\_______| \____$$ |\__| \_______|      \________|\____$$ | \_______|
                   $$\   $$ |                             $$\   $$ |          
                   \$$$$$$  |                             \$$$$$$  |          
                    \______/                               \______/         
                                                                      
```

<div align="center">

![Python 3.5](https://img.shields.io/badge/Python-3.6%2B-blue.svg)
![OS Linux](https://img.shields.io/badge/Supported%20OS-Linux-yellow.svg)
![Lets stalk](https://img.shields.io/badge/Stalkermode-Activated-red.svg)

</div>

---

<p align="center"> You have at least one image of the person you are looking for and a clue about their name. 
<br>
You enter this data into EagleEye and it tries to find Instagram, Youtube, Facebook, and Twitter Profiles of this person.
    <br> 
</p>

## 📝 Table of Contents
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](#todo)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)


## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- A system with a x-server installed (Linux)
- Firefox installed

#### When using docker
- Only docker is required

#### When you dont use docker
- Python 3.6 or higher
- Pythons pip


### Installing

#### Docker (Preferred)
**Make sure that you have docker installed**
**Make sure that you use a LINUX distribution as the host**
1. Clone the Repository

   ``` $ git clone https://github.com/ThoughtfulDev/EagleEye ```
2. ```
   $ cd EagleEye
   $ sudo docker build -t eagle-eye .
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

---

#### Automated Prerequisites Installation (If Docker doesn't work)
```
wget https://raw.githubusercontent.com/ThoughtfulDev/EagleEye/master/install.sh && chmod +x install.sh && ./install.sh
```

---

#### Manual Prerequisites Installation (If you are hardcore)

For **Debian** based Distros
```
$ sudo apt update && sudo apt upgrade -y
$ sudo apt install git python3 python3-pip python3-dev
$ sudo apt install libgtk-3-dev libboost-all-dev build-essential cmake libffi-dev
$ git clone https://github.com/ThoughtfulDev/EagleEye
$ cd EagleEye && python3 -m pip install --user -r requirements.txt
$ python3 -m pip install --user --upgrade beautifulsoup4 html5lib spry
```

For **Arch**
```
$ sudo pacman -Syu
$ sudo pacman -S git python python-pip gtk3 boost cmake libffi
$ git clone https://github.com/ThoughtfulDev/EagleEye
$ cd EagleEye && python3 -m pip install --user -r requirements.txt
$ python3 -m pip install --user --upgrade beautifulsoup4 html5lib spry
```


If Firefox is installed, download the [latest release](https://github.com/mozilla/geckodriver/releases/latest) of the Geckodriver for you Architecture.

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


## 🎈 Usage <a name="usage"></a>

### Configuration: General

Change the value in `config.json` to the path of the `geckodriver` e.g
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

Put at least one Image of the Person you want to find in the `known` folder.

Supported Filetypes are: **jpg/JPG, jpeg/JPEG, png/PNG, and bmp/BMP.**

### Run

Then run the program ;)
```
$ python3 eagle-eye.py
```

To see a list of all available Options just type
```
$ python3 eagle-eye.py -h
```

*The ImageRaider Reverse Image Search can take some minutes 1-15 Minutes depending on the count of Images*


## TODO <a name = "todo"></a>
* Implement the Chrome Webdriver

## ⛏️ Built Using <a name = "built_using"></a>
- [Python](https://www.python.org/) - Language
- [dlib](http://dlib.net/) - Face detection
- [face_recognition](https://github.com/ageitgey/face_recognition) - dlib python api
- [Selenium](https://www.seleniumhq.org/) - WebBrowser automation

## ✍️ Authors <a name = "authors"></a>
- [@ThoughtfulDev](https://github.com/ThoughtfulDev) - Idea & Work

## 🎉 Acknowledgements <a name = "acknowledgement"></a>
- The movie Eagle Eye
