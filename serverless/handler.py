import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('ConnectedDevicesTable')
    scan = table.scan()
    data = scan['Items']

    devices = {}

    for x in data:
        if x == "ID":
            devices.append(x['ID'])
        print(x)
        
    return json.dumps({"Devices": devices})