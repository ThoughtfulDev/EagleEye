#!/usr/bin/env python3

import os
import tempfile
from collections import Counter
from pathlib import Path
import utils.console as console
import utils.config as cfg
from grabber.facebook import FBGrabber
from grabber.google import GoogleGrabber
from grabber.yandex import YandexGrabber
from grabber.imageraider import ImageRaiderGrabber
from face_recog import FaceRecog
from instaLooter import InstaLooter
from report.report import makeReport


def presentResult(predictions):
    argmax = Counter(predictions)
    console.section("Result")
    (most_common_str, _) = argmax.most_common(n=1)[0]
    console.task("Google says it could be: {0}".format(most_common_str))

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
    looter = InstaLooter(profile=username)
    images = []
    i = 0
    for media in looter.medias():
        if i > cfg.instaLimit():
            break
        if not media['is_video']:
            console.subtask("Got Image: {0}".format(media['display_src'].strip()[:90]))
            images.append(media['display_src'])
            i = i + 1
    return images

def main():
    # collect user input
    console.prompt('Enter the persons name to find on FB: ')
    name = input('')

    console.prompt('How many jitters, higher is better [max 100]: ')
    num_jitters = input('')
    num_jitters = int(num_jitters)
    if num_jitters > 100:
        console.subfailure('Dude wtf?!')
        num_jitters = 100
        console.subfailure('Using 100 jitters...')

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

    # google reverse image search on profile pics
    g = GoogleGrabber()
    for img in profile_imgs:
        g.collectLinks(img)

    # google reverse image search on reference pic
    g.collectLinksLocal()
    rev_links, predictions = g.finish()

    yandex = YandexGrabber()
    for img in profile_imgs:
        yandex.collectLinks(img)
    
    #add to rev_links
    for e in yandex.finish():
        rev_links.append(e)
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
        console.failure('No Links founds...')
    else:
        raider = ImageRaiderGrabber()
        raider.insertImageLinks(raider_img_list)
        raider.downloadCSV()
        raider_links = raider.processCSV()
        for raider_link in raider_links:
            rev_links.append(raider_link)


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
    main()
