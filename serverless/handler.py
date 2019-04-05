import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('ConnectedDevicesTable')
    response = table.scan()
    data = response['Items']
    print(data)
    return json.dumps(data)
