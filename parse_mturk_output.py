def parse_presigned_s3url(url):
    """ parses a presigned s3 url
    args:
        url: string

    returns:
        s3bucket: string
        video_uuid: string
        start_frame: int
        end_frame: int

    example:
    bucket, uuid, start, end = parse_presigned_s3url(
        'https://kinetic-mechanical-twerk.s3.amazonaws.com/99ae0ca7-f727-43a8-ae72-4e2cd9115947/gifs/frame_61_to_90.gif?AWSAccessKeyId=AKIAIIVU4DWJCSWJPVNA&Signature=b3fZWg55776TjgCcHFGvMtgzWEk%3D&Expires=1534002311'
    )
    print(bucket)
    > 'kinetic-mechanical-twerk'
    print(uuid)
    > '99ae0ca7-f727-43a8-ae72-4e2cd9115947
    print(start)
    > 61
    print(end)
    > 90
    """
    if url[:8]=='https://':
        url = url[8:]
    url = url.split('?')[0]
    temp = url.split('/')
    assert(temp[2]=='gifs')
    assert(temp[3][:6]=='frame_')
    assert('_to_' in temp[3])
    bucket = temp[0].replace('.s3.amazonaws.com','')
    video_uuid = temp[1]
    string = temp[3][6:]
    string = string.replace('.gif','')
    start_frame, end_frame = map(int,string.split('_to_'))
    return bucket, video_uuid, start_frame, end_frame

def annotate_scarif_video(uuid, start, end, label, assignmentId):
    """annotates a video in scarif using bravado.
    args:
        uuid: scarif video uuid (string)
        start: start frame (int)
        end: end frame (int)
        label: string
        assignmentId: AMT assignmentId (string)

    return:
        response: response of swagger client
            http://scarif-api.staging.wearkinetic.com/swagger.json

    side effects:
        a new entry is placed in the videoAnnotations table in scarif
    """
    # query to check that we've not already uploaded this annotation
    query = 'SELECT * FROM \"videoAnnotation\" WHERE label ~\'{:s}\''.format(assignmentId)
    import pg8000
    from os import environ as env
    conn = pg8000.connect(
        user=env['SCARIF_USER'],
        host=env['SCARIF_HOST'],
        database='scarif',
        password=env['SCARIF_PASS']
    )
    cursor = conn.cursor()
    cursor.execute(query)
    response = cursor.fetchone()
    cursor.close()
    conn.close()

    if response != None:
        print('annotation is already present',file=sys.stderr)
        return response[0]

    #EXAMPLE CURL COMMAND
    #curl -X POST "http://scarif-api.wearkinetic.com/v1/annotate/video" -H "accept: application/json" -H "api_key: asdasd" -H "Content-Type: application/json" -d "{ \"end_time\": 0, \"label\": \"string\", \"start_time\": 1, \"target_uuid\": \"b607a3c1-87d1-417d-afa5-972ab2ce694f\"}"
    from bravado.requests_client import RequestsClient
    from bravado.client import SwaggerClient
    import json
    http_client = RequestsClient()
    http_client.set_api_key(
        'scarif-api.wearkinetic.com', 'LITERALLY ANY STRING',
        param_name='api_key', param_in='header'
    )
    client = SwaggerClient.from_url(
        'http://scarif-api.wearkinetic.com/swagger.json',
        http_client=http_client
    )
    label_aug = json.dumps({'label':label, 'assignmentId':assignmentId})
    ann = client.get_model('Annotation')(
        label=label_aug,
        start_time=start,
        end_time=end,
        target_uuid=uuid
    )
    return client.annotations.annotate(type='video', body=ann).result()

if __name__ == '__main__':
    import sys
    mturk_output_fn = sys.argv[1]
    with open(mturk_output_fn,'r') as f:
        import csv
        reader = csv.DictReader(f)
        for row in reader:
            assignmentId = row['AssignmentId']
            if row['Approve'] != 'Approved':
                print('skipping {:s} with status {:s}'.format(assignmentId, str(row['Approve'])))
                continue
            url = row['Input.image_url']
            label = row['Answer.categories']
            bucket, uuid, start, end = parse_presigned_s3url(url)
            response = annotate_scarif_video(uuid, start, end, label, assignmentId)
            print(response)
            break
