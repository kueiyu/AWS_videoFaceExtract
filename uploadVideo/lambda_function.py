import json
import dynamoDB as db
from dataToHTML import *

html_upper = ['head.htm', 'form.htm', 'tableHead.htm']
html_lower = ['tail.htm']

video_path = 'http://upload-for-public.s3.amazonaws.com/'
face_path = 'http://extracted-face.s3.amazonaws.com/'



def lambda_handler(event, context):
    video_metadata = db.getDataOfVideosAndFaces()   # Query dynamoDB to retrieve metadata
    #print(json.dumps(video_metadata, indent=4))

    html_content = ''
    for html in html_upper:                         # Combine all HTML files
        with open('HTML/'+html, 'r') as f:
            html_content += f.read()
    
    html_content += htmlTableBody(video_metadata, video_path, face_path)
    
    for html in html_lower:                         # Combine all HTML files
        with open('HTML/'+html, 'r') as f:
            html_content += f.read()
    
    return {
        'statusCode': 200,
        'body': html_content,
        "headers": {
        'Content-Type': 'text/html',
        }
    }
