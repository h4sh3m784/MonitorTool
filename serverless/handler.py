import json
import boto3

def handler(event, contedict):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('ConnectedDevicesTable')
    scan = table.scan()
    data = scan['Items']

    devices = []

    for d in data:
        devices.append(d['ID'])
        
    return json.dumps({"Devices": devices})