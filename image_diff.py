# USAGE

# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
#from flask import Flask, request #import main Flask class and request object
from PIL import Image
import numpy as np
#import flask
import io, os, sys
import datetime

import flask
import cv2
import base64
sys.path.append(".")
import tkinter
#import cv2
import imutils
from security import authenticate, identity

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'ch@ngEp0nd'
api = Api(app)

jwt = JWT(app, authenticate, identity)


         

class ImageDifference(Resource):
    #@app.route('/')
    @jwt_required()
    def post(self):
        image1= request.files['imageA1']  
        image1.save(image1.filename)  
        imageA = cv2.imread(image1.filename)
        
        image2= request.files['imageB2']  
        image2.save(image2.filename)  
        imageB = cv2.imread(image2.filename)
        
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        # compute the Structural Similarity Index (SSIM) between the two
        # images, ensuring that the difference image is returned
        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        print("SSIM: {}".format(score))
        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
        path = 'C:/Users/malini.d/Desktop/API_tm_SSIM/SSIM_API/Saved_images'
        # show the output images

        cv2.imshow("First_image", imageA)
        cv2.imshow("Second_image", imageB)
        #cv2.imshow("Diff", diff)
        #cv2.imshow("Thresh", thresh)
        cv2.waitKey(0)
        cv2.imwrite(os.path.join(path , image1.filename), imageA)
        cv2.imwrite(os.path.join(path , image2.filename), imageB)
        #cv2.imwrite(os.path.join(path , 'Diff.jpg'), diff)
        #cv2.imwrite(os.path.join(path , 'Thresh.jpg'), thresh)
        cv2.waitKey(0)
        return 'File Saved Successfully!!!'

	
api.add_resource(ImageDifference, '/imgdiff')

if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True
		