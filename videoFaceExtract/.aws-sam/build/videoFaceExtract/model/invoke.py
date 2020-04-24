import json
import boto3

def callAgePrediction(video_filename: str, face_bucket: str, face_image_filenames: list):
    
    metadata = {
        'video_filename': video_filename,
        'face_bucket': face_bucket,
        'face_filenames': face_image_filenames
    }
    
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName='ageByRekognition',
        InvocationType='Event',  # asynchronously
        Payload = json.dumps(metadata)
    )
    
    return
