#!/bin/bash
# Downgrade fake-useragent to a version compatible with Python 3.8
pip3 install "fake-useragent<1.4.0" selenium

# Fix Geckodriver path: Create symlink if missing in /usr/bin but found in /usr/local/bin
if [ ! -f "/usr/bin/geckodriver" ] && [ -f "/usr/local/bin/geckodriver" ]; then
    ln -s /usr/local/bin/geckodriver /usr/bin/geckodriver
fi

cd /EagleEye
TARGET_NAME=${NAME:-"Kristina"}
python3 eagle-eye.py --docker --name "$TARGET_NAME"

#now copy the result
yes | cp -rf /EagleEye/*.pdf /result/
