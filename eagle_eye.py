#!/usr/bin/env python3

import os
import sys
import tempfile
import argparse
from collections import Counter
from pathlib import Path
import utils.console as console
import utils.config as cfg
from grabber.facebook import FBGrabber, FBProfileGrabber
from grabber.google import GoogleGrabber
from grabber.instagram import InstagramGrabber
from face_recog import FaceRecog
import subprocess
import json
import shutil
from report.report import makeReport, makeJSONReport


def presentResult(predictions):
    if len(predictions) > 0:
        argmax = Counter(predictions)
        console.section("Result")
        if len(argmax.most_common(n=1)) > 0:
            (most_common_str, _) = argmax.most_common(n=1)[0]
        else:
            most_common_str = 'None'
        console.task("Google says it could be: {0}".format(most_common_str))
    else:
        console.failure("No predictions found")


def filterInstaLinks(links):
    r = []
    for l in links:
        if "www.instagram.com" in l:
            r.append(l)
    return r


def parseInstaUsername(links):
    usernames = []
    for l in links:
        a = l[8:]
        a = a.split('/')
        if len(a) >= 2:
            if len(a[1]) >= 4:
                usernames.append(a[1])
        else:
            console.subfailure('Error parsing {0}'.format(l))
    return usernames


def validateInstaUser(username, num_jitters):
    images = getInstaLinks(username)
    # print(images)
    if len(images) >= cfg.instaLimit():
        images = images[:cfg.instaLimit()]
    r = FaceRecog(username, images, num_jitters=num_jitters)
    r.loadKnown(username)
    profile_links, _ = r.getValidLinksAndImg(username)
    return len(profile_links) > 0


def getInstaLinks(username):
    instagrabber = InstagramGrabber(username)
    return instagrabber.getLinks()


def main(skipFB=False, FBUrls=[], jsonRep=None, dockerMode=False, dockerName=None):
    if not skipFB:
        # collect user input
        if dockerMode:
            console.section("Running in DOCKER MODE")
            name = dockerName
        else:
            console.prompt('Enter the persons name to find on FB: ')
            name = input('')
            while not name:
                console.prompt('Enter the persons name to find on FB: ')
                name = input('')
    else:
        console.task('Skipping FB Search')
        name = "Unknown"

    if dockerMode:
        console.task('Skipping jitters since specified in config.json')
        num_jitters = cfg.jitters()
    else:
        console.prompt(
            'How many jitters, higher is better [max 100] (default=70): ')
        num_jitters = input('')
    if not num_jitters:
        console.task('Settings jitters to 70')
        num_jitters = 70
    num_jitters = int(num_jitters)
    if num_jitters > 100:
        console.subfailure('Dude wtf?!')
        num_jitters = 100
        console.subfailure('Using 100 jitters...')

    if not skipFB:
        # grab profile urls
        f = FBGrabber(name)
        f.grabData()
        # do face recognition on those profile images
        r = FaceRecog(f.getProfileLinks(), f.getProfileImages(),
                      num_jitters=num_jitters)
        r.loadKnown(name)
        profile_links, profile_imgs = r.getValidLinksAndImg(name)
        console.section('Result')
        console.task('Found the following Profiles:')
        for i in range(len(profile_links)):
            console.subtask(profile_links[i])
    else:
        if len(FBUrls) > 0:
            f = FBProfileGrabber(FBUrls)
            img_urls = f.grabLinks()
            # FBURLS are our profile links synchron with img_urls
            # so FBURLS[0] <=> img_urls[0]
            r = FaceRecog(FBUrls, img_urls, num_jitters=num_jitters)
            r.loadKnown(name)
            profile_links, profile_imgs = r.getValidLinksAndImg(name)
            console.section('Result')
            console.task('Found the following Profiles:')
            for i in range(len(profile_links)):
                console.subtask(profile_links[i])
        else:
            profile_links = []
            profile_imgs = []

    # google reverse image search on profile pics
    g = GoogleGrabber()
    for img in profile_imgs:
        g.collectLinks(img)

    # google reverse image search on reference pic
    g.collectLinksLocal()
    rev_links, predictions = g.finish()

    rev_links = list(set(rev_links))

    instaNames = parseInstaUsername(filterInstaLinks(rev_links))
    validatedInstaNames = []
    console.section("Validating Instagram Profiles")
    for un in instaNames:
        console.task("Validating Profile: '{0}'".format(un))
        if validateInstaUser(un, num_jitters):
            validatedInstaNames.append(un)

    raider_img_list = profile_imgs
    for v in validatedInstaNames:
        l = getInstaLinks(v)

        for li in l:
            raider_img_list.append(li)

    rev_links = list(set(rev_links))
    predictions = list(set(predictions))
    console.section('Links')
    print(rev_links)
    console.section('Predictions')
    try:
        predictions = [x.lower() for x in predictions]
    except:
        predictions = []
    print(predictions)
    presentResult(predictions)

    for pl in profile_links:
        rev_links.append(pl)
    rev_links = list(set(rev_links))

    if jsonRep:
        console.section("Dumping JSON Report")
        makeJSONReport(name, rev_links, predictions,
                       validatedInstaNames, jsonRep)
    else:
        console.section("Creating PDF Report")
        makeReport(name, rev_links, predictions, validatedInstaNames)

    p = os.path.join(tempfile.gettempdir(), 'imageraider')
    if os.path.isdir(p):
        pathlist = Path(p).glob('**/*')
        for path in pathlist:
            s_p = str(path)
            os.remove(s_p)
    console.task("KTHXBYE")


if __name__ == "__main__":
    console.banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-sFB', '--skipfb', action='store_true',
                        help='Skips the Facebook Search')
    parser.add_argument('-d', '--docker', action='store_true',
                        help='Set this flag if run in docker mode')
    parser.add_argument('-n', '--name', nargs='?',
                        help='Specify the persons name. Only active with the --docker flag')
    parser.add_argument('-json', '--json', nargs='?',
                        help='Generates a json report. Specify a Filename')
    parser.add_argument('-fbList',
                        '--facebookList',
                        nargs='?',
                        help="A file which contains Links to Facebook Profiles. '--skipfb' options must be enabled to use this")
    args = parser.parse_args()

    if args.docker:
        aDocker = args.docker
        if args.name:
            aName = args.name
        else:
            console.failure("Please supply a name using the --name flag")
            sys.exit(-2)
    else:
        aName = None
        aDocker = False

    if args.json:
        jsonRepFile = args.json
        if os.path.isfile(jsonRepFile):
            console.failure("File '{}' already exists".format(jsonRepFile))
            sys.exit(-1)
    else:
        jsonRepFile = None

    if args.facebookList and args.skipfb:
        if os.path.isfile(args.facebookList):
            with open(args.facebookList, 'r') as f:
                content = f.readlines()
            content = [x.strip() for x in content]
            main(skipFB=args.skipfb, FBUrls=content, jsonRep=jsonRepFile,
                 dockerMode=aDocker, dockerName=aName)
        else:
            console.failure(
                "File '{}' does not exist".format(args.facebookList))
            sys.exit(-1)
    else:
        main(skipFB=args.skipfb, FBUrls=[], jsonRep=jsonRepFile,
             dockerMode=aDocker, dockerName=aName)
