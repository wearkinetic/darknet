import boto3
import sys, os

uuid = sys.argv[1]

# Get the service client.
s3 = boto3.client('s3')
N_hours = 24
url_list = list()

directory = '{:s}/gifs'.format(uuid)
for fn in os.listdir(directory):
    key = os.path.join(directory,fn)
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'kinetic-mechanical-twerk',
            'Key': key
        },
        ExpiresIn=60*60*N_hours
    )
    url_list.append(url)

with open('{:s}/media-links.csv'.format(uuid),'w') as f:
    import csv
    writer = csv.writer(f)
    writer.writerow(['media-links'])
    for url in url_list:
        writer.writerow([url,])
