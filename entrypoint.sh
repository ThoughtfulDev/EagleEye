#!/bin/sh

python /app/eagle_eye/eagle_eye.py --docker --name "${@}"

#now copy the result
# yes | cp -rf ./known/*.pdf ./result/