from flask import Flask, render_template, request, jsonify 
from werkzeug import secure_filename
import boto3
import io
from PIL import Image
from flaskFaceSearch import *
import os
import requests
import json
import yaml
import argparse
from helper import *
import sys
import time
from microidentifyFace import *
from hvHelper import *;

groupIdHV = "group1"
testPath = "images"

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
face = Flask(__name__, template_folder=template_path)

@face.route('/')
def hello_world():
    return "Welcome to future "

@face.route('/FR')
def faceRec():
    arg = request.args
    method = arg['algo']
    

    url = "https://s3.amazonaws.com/tempReco/"+arg['file']
    r = requests.get(url, allow_redirects=True)
    open('images/pic.jpg', 'wb').write(r.content)

    fileLoc = 'images/pic.jpg'

    #print(fileLoc)
    if(method.lower()=="ms"):
        t1 = time.time()
        MicrofaceId = detectFace(url)
        #print MicrofaceId
        toReturnMicrosoft = str(identifyFace(MicrofaceId)["personId"])
        t2 = time.time()
        #toReturnMicrosoft+= " TimeTaken: "+str(t2-t1)
        print toReturnMicrosoft
        return jsonify(status="success", result=toReturnMicrosoft)

    if(method.lower()=="aws"):
        t1 = time.time()
        toReturnAWS = str(search(fileLoc))

        t2 = time.time()
        #toReturnAWS+=" TimeTaken: "+str(t2-t1)
        return jsonify(status="success", result=toReturnAWS)

    if(method.lower()=="hv"):
        t1 = time.time()
        BATCH_SIZE = 100
        facePaths = getFacePaths(testPath)
        res = faceRecognize(facePaths, groupIdHV, BATCH_SIZE)
        toReturnHV = str(res["result"][0][0]["personId"])
        t2 = time.time()
        print toReturnHV
        #toReturnHV += " TimeTaken: "+str(t2-t1)
        
        return jsonify(status="success", result=toReturnHV)

if __name__ == '__main__':
    face.run(host='0.0.0.0')
