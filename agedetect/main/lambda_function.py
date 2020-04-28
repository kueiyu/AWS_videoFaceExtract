import boto3
import math
import cv2
import numpy as np
import json
import dynamoDB as db

# import requests
s3 = boto3.client('s3')
download_path = '/tmp/'
def lambda_handler(event, context):
    
    # image imput info
    video_filename = event['video_filename']
    source_bucket = event['face_bucket']
    face_filenames = event['face_filenames']
    
    age = ''
    
    # Model Source
    ageProto='main/age_deploy.prototxt'
    ageModel='main/age_net.caffemodel'
    
    MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
    ageList=['0-2', '4-6', '8-12', '15-20', '25-32', '38-43', '48-53', '60-100']
    genderList=['Male','Female']
        
    ageNet=cv2.dnn.readNet(ageModel,ageProto)
    print('Model init complete')
    
    for face in face_filenames:
        resp = s3.get_object(Bucket=source_bucket, Key=face)
        s3.download_file(source_bucket,face,download_path+face)
        video=cv2.VideoCapture(download_path + face)
        ret, frame = video.read()
        blob=cv2.dnn.blobFromImage(frame, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        ageNet.setInput(blob)
        agePreds=ageNet.forward()
        age += '{},'.format(ageList[agePreds[0].argmax()])
    
    print(video_filename, age)
    
    r = db.AddAttrToItemInDB(video_filename, 'face_ages2', age) # Add face ages to DB
    print(r)
    
    return 'Age prediction finished.'
