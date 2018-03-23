import cv2
import face_recognition
from urllib.request import urlretrieve
from pathlib import Path
import os
import tempfile
from sys import platform
import random
import string
import utils.console as console


class FaceRecog:
    def __init__(self, profile_list, profile_img, num_jitters=10):
        self.profile_list = profile_list
        self.profile_img = profile_img
        self.num_jitters = num_jitters
        self.known_face_encodings = []
        self.known_face_names = []
        console.section('Starting Face Recognition')

    def loadKnown(self, label):    
        console.task('Loading known faces')
        pathlist = Path('./known').glob('**/*.jpg')
        for path in pathlist:
            p_str = str(path)
            delim = '/'
            if platform == "win32":
                delim = '\\'
            console.subtask('Loading {0}'.format(p_str.split(delim)[1]))
            im = face_recognition.load_image_file(p_str)
            encoding = face_recognition.face_encodings(im, num_jitters=self.num_jitters)
            for e in encoding:
                self.known_face_encodings.append(e)
                self.known_face_names.append(label)

    def constructIndexes(self, label):
        valid_links = []
        console.section('Analyzing')
        file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        file_name += '.jpg'
        tmp_path = os.path.join(tempfile.gettempdir(), file_name)
        console.task("Storing Image in {0}".format(tmp_path))
        for num, i in enumerate(self.profile_img):
            console.task('Analyzing {0}...'.format(i.strip()[:90]))
            urlretrieve(i, tmp_path)
            frame = cv2.imread(tmp_path)
            big_frame = cv2.resize(frame, (0, 0), fx=2.0, fy=2.0)
            rgb_small_frame = big_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations, num_jitters=self.num_jitters)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                face_names.append(name)

            for _, name in zip(face_locations, face_names):
                if name == label:
                    valid_links.append(num)
        if os.path.isfile(tmp_path):
            console.task("Removing {0}".format(tmp_path))
            os.remove(tmp_path)
        return valid_links
    
    def getValidLinksAndImg(self, label):
        if len(self.known_face_encodings) <= 0:
            console.failure('No Face Encodings found!')
            console.failure('Did you call `loadKnown(label)` before calling this method?')
            return []
        valid_url = []
        valid_img = []
        valid_indexes = self.constructIndexes(label)
        for index in valid_indexes:
            valid_url.append(self.profile_list[index])
            valid_img.append(self.profile_img[index])
        return valid_url, valid_img
