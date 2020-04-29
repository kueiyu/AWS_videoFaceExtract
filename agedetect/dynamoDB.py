import json
import boto3

client = boto3.client('dynamodb')

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
