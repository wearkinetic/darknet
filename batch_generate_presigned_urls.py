import boto3
import sys, os

uuid_file = sys.argv[1] # Should be a txt file where each line is a video uuid

# Get the service client.
s3 = boto3.client('s3')
N_hours = 24
url_list = list()

with open(uuid_file,'r') as f:
    for uuid in f.readlines():
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

base, _ = os.path.splitext(uuid_file)
with open('{:s}_mturk_input.csv'.format(base),'w') as f:
    import csv
    writer = csv.writer(f)
    writer.writerow(['image_url'])
    for url in url_list:
        writer.writerow([url,])
