import boto3
import sys, os
input_fn = sys.argv[1]
uuid,_ = os.split(input_fn)
with open(input_fn,'r') as f:
    import json
    keys = json.load(input_fn)

# Get the service client.
s3 = boto3.client('s3')
N_hours = 24*3
url_list = list()

for key in keys:
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'kinetic-mechanical-twerk',
            'Key': key
        },
        ExpiresIn=60*60*N_hours
    )
    url_list.append(url)

with open('{:s}/media-links.csv','w') as f:
    import csv
    writer = csv.writer(f)
    writer.writerow('media-links')
    for url in url_list:
        writer.writerow(url)
