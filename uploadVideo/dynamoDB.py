import boto3

client = boto3.client('dynamodb')

def getDataOfVideosAndFaces(table_name='videoFace'):
    results = client.scan(
        TableName=table_name,
    )
    results = results['Items']
    output = []
    for result in results:
        video_filename = result.get('video_filename', {'S': ''})['S']
        upload_date = result.get('uploadDate', {'S': ''})['S']
        process_date = result.get('processDate', {'S': 'Processing'})['S']
        face_filenames = result.get('faceFileNames', {'SS': []})['SS']
        output.append({
                'video_filename': video_filename,
                'uploadDate': upload_date,
                'processDate': process_date,
                'faces': face_filenames,
        })
    return output