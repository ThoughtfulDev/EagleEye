#!/usr/bin/env python3

import os, sys
import tempfile
import argparse
from collections import Counter
from pathlib import Path
import utils.console as console
import utils.config as cfg
from grabber.facebook import FBGrabber, FBProfileGrabber
from grabber.google import GoogleGrabber
from grabber.yandex import YandexGrabber
from grabber.imageraider import ImageRaiderGrabber
from grabber.pictriev import PictrievGrabber
from grabber.instagram import InstagramGrabber
from face_recog import FaceRecog
from pathlib import Path
import subprocess, json, shutil
from report.report import makeReport


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
        if "instagram.com" in l:
            r.append(l)
    return r

def parseInstaUsername(links):
    usernames = []
    for l in links:
        a = l[8:]
        a = a.split('/')
        if len(a) >= 2:
            usernames.append(a[1])
        else:
            console.subfailure('Error parsing {0}'.format(l))
    return usernames


def validateInstaUser(username, num_jitters):
    images = getInstaLinks(username)
    r = FaceRecog(username, images, num_jitters=num_jitters)
    r.loadKnown(username)
    profile_links, _ = r.getValidLinksAndImg(username)
    return len(profile_links) > 0

def getInstaLinks(username):
    instagrabber = InstagramGrabber(username)
    return instagrabber.getLinks()

def main(skipFB=False, skipIR=False, skipY=False, FBUrls=[]):
    if not skipFB:
        # collect user input
        console.prompt('Enter the persons name to find on FB: ')
        name = input('')
    else:
        console.task('Skipping FB Search')
        name = "Unknown"

    console.prompt('How many jitters, higher is better [max 100]: ')
    num_jitters = input('')
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
        r = FaceRecog(f.getProfileLinks(), f.getProfileImages(), num_jitters=num_jitters)
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
            #FBURLS are our profile links synchron with img_urls
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

    #TODO: Fix yandex search
    #if not skipY:
    if False:
        yandex = YandexGrabber()
        for img in profile_imgs:
            yandex.collectLinks(img)
        yandex.collectLinksLocal()
        #add to rev_links
        for e in yandex.finish():
            rev_links.append(e)
    else:
        console.task('Skipping Yandex Search')
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

    if len(raider_img_list) <= 0:
        console.failure('No Links found...')
    else:
        if not skipIR:
            raider = ImageRaiderGrabber()
            raider.insertImageLinks(raider_img_list)
            raider.downloadCSV()
            raider_links = raider.processCSV()
            for raider_link in raider_links:
                rev_links.append(raider_link)
        else:
            console.task('Skipping ImageRaider Search')


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

    #estimate age
    ageEstimator = PictrievGrabber()
    if len(validatedInstaNames) > 0:
        for v in validatedInstaNames:
            l = getInstaLinks(v)
            for li in l:
                ageEstimator.collectAges(li)
        age = ageEstimator.finish()
    else:
        console.failure('No Instagram Images to upload...')
        ageEstimator.finish()
        age = "Unknown"

    console.section("Creating PDF Report")
    makeReport(name, rev_links, predictions, validatedInstaNames, age)


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
    parser.add_argument('-sFB', '--skipfb', action='store_true', help='Skips the Facebook Search')
    parser.add_argument('-sIR', '--skipir', action='store_true', help='Skips the ImageRaider Reverse Search')
    #parser.add_argument('-sY', '--skipyandex', action='store_true', help='Skips the Yandex Reverse Search')
    parser.add_argument('-fbList', 
                        '--facebookList', 
                        nargs='?', 
                        help="A file which contains Links to Facebook Profiles. '--skipfb' options must be enabled to use this" )
    args = parser.parse_args()

    if args.facebookList and args.skipfb:
        if os.path.isfile(args.facebookList):
            with open(args.facebookList, 'r') as f:
                content = f.readlines()
            content = [x.strip() for x in content] 
            #TODO: fix yandex
            #main(skipFB=args.skipfb, skipIR=args.skipir, skipY=args.skipyandex, FBUrls=content)
            main(skipFB=args.skipfb, skipIR=args.skipir, skipY=None, FBUrls=content)
        else:
            console.failure("File '{}' does not exist".format(args.facebookList))
            sys.exit(-1)
    else:
        #TODO: fix yandex
        #main(skipFB=args.skipfb, skipIR=args.skipir, skipY=args.skipyandex, FBUrls=[])
        main(skipFB=args.skipfb, skipIR=args.skipir, skipY=None, FBUrls=[])
