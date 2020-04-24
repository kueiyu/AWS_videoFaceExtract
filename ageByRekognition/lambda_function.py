import json
import boto3
import dynamoDB as db

client = boto3.client('rekognition')

def lambda_handler(event, context):

    video_filename = event['video_filename']
    source_bucket = event['face_bucket']
    face_filenames = event['face_filenames']
    
    age_results = ''  # DyanmoDB not allow duplicate string elemenst, combine all ages intto a string separated by comma
    
    for face in face_filenames:
        response = client.detect_faces(
            Image={
                'S3Object': {
                'Bucket': source_bucket,
                'Name': face,
                },
                
            },
            Attributes=['ALL']
        )
        
        try:
            age_range = response['FaceDetails'][0]['AgeRange']
            age_results += '{}-{} Y/O,'.format(age_range['Low'], age_range['High'])
        except:
            age_results += 'Age unknown,'
        
    print(video_filename, age_results)
    
    r = db.AddAttrToItemInDB(video_filename, 'face_ages', age_results) # Add face ages to DB
    print(r)
    
    return 'Age prediction finished.'
