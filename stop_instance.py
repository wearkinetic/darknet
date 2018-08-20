import boto3
ec2 = boto3.resource('ec2')
instance = ec2.Instance('i-030727c9c67024b54')
instance.stop()
instance.wait_until_stopped()
print('Instance stopped')
