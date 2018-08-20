import boto3
ec2 = boto3.resource('ec2')
instance = ec2.Instance('i-030727c9c67024b54')
if instance.state['Name'] == 'Stopped':
    instance.start()
instance.wait_until_running()
print(instance.public_dns_name)
