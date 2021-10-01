import csv
import glob
import boto3
import json
import os

with open('credentials.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]

client = boto3.client('rekognition', 
        region_name='us-east-1', 
        aws_access_key_id=access_key_id, 
        aws_secret_access_key=secret_access_key)

responses = []
path = glob.glob('./images/*.jpg');
for file in path:
    with open(file, 'rb') as source_image:
        source_byte = source_image.read()
    response = client.detect_labels(Image={'Bytes': source_byte}, MaxLabels = 10, MinConfidence = 95)
    jsonPath = os.path.splitext('./json/' + file[9:])[0] + '.json'
    with open(jsonPath, 'w') as f:
            json.dump(response, f, indent=4 )
