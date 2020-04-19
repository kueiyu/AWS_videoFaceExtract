import json
import boto3

client = boto3.client('dynamodb')

def putVideoInfoToDB(video_filename, create_date, table_name='videoFace', primary_key='video_filename'):
    client.put_item(
        TableName=table_name,
        Item={
                primary_key: {
                  'S': video_filename
                },
                'uploadDate': {
                    'S': create_date
                },
            }
    )
    return 'Add record of new video into dynamoDB'


def AddAttrToItemInDB(video_filename, attr_name: str, attr_content: str, table_name='videoFace', primary_key='video_filename'):
    data_type = 'SS' if type(attr_content).__name__ == 'list' else 'S'
    client.update_item(
        TableName=table_name,
        Key={
            primary_key: {
                'S': video_filename
            }
        },
        AttributeUpdates={
            attr_name: {
                'Value': {
                    data_type: attr_content
                }
            }
        }
    )
    return "Add data to item in DB"