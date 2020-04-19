import os
import sys
import boto3
from datetime import datetime
import time
from urllib.parse import unquote_plus
from model import dynamoDB as db


s3_client = boto3.client('s3')

bucket_results = 'extracted-face'
download_path = '/tmp/'
upload_path = '/tmp/'

face_recog_models = [    # model names in face_recognition_models
    'dlib_face_recognition_resnet_model_v1.dat',
    'mmod_human_face_detector.dat',
    'shape_predictor_5_face_landmarks.dat',
    'shape_predictor_68_face_landmarks.dat'
]

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']            # Get the triggering bucket name
        key = unquote_plus(record['s3']['object']['key'])  # Get the target file name
        print(bucket, key)

        r = db.putVideoInfoToDB(key, datetime.now().strftime("%m-%d-%Y %T"))  # Add record of this new video into database
        print(r)

        """
        Because the models for face_recognition are too huge (>100MB), the overall size of lambda package will > 250MB
        -> Put all those models to S3, then download them during runtime
        """
        for model_name in face_recog_models:  # Download face_recognition_models form S3 bucket
            s3_client.download_file('face-recog-models', 'models/'+ model_name, download_path + model_name)
        """
        only /tmp/ allow to write in AWS, so downlaod to it. 
        See https://stackoverflow.com/questions/39383465/python-read-only-file-system-error-with-s3-and-lambda-when-opening-a-file-for-re
        """
        print('Face models downloaded')

        from model import face_extract  # Can only works if models were succesfully downloaded
        print('Import face_extract')

        s3_client.download_file(bucket, key, download_path + key)  # Download the videos
        print('Source video downloaded')

        face_image_filenames = face_extract.extractFaces(download_path, key, upload_path)
        print('Face extraction completed')

        r = db.AddAttrToItemInDB(key, 'processDate', datetime.now().strftime("%m-%d-%Y %T")) # Add date of processing to DB
        r = db.AddAttrToItemInDB(key, 'faceFileNames', face_image_filenames) # Add face filenames to DB
        print(r)

        for image_name in face_image_filenames:
            s3_client.upload_file(upload_path + image_name, bucket_results, image_name)
        print("Face images saved to S3")

    return "Finished"