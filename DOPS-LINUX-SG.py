import boto3
from botocore.exceptions import ClientError
import sys
import csv


region = ['us-east-1', 
        'us-east-2', 
        'us-west-1', 
        'us-west-2',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3']

group_name = 'DOPS-LINUX-SG'

csv_name = '{0}{1}'.format(group_name, '.csv')


#aws_access_key = sys.argv[1]
#aws_secret_key = sys.argv[2]

count1 = len(region)

print(group_name)

for z in range(0,count1):


    ec2 = boto3.resource('ec2',
                #aws_access_key_id = aws_access_key ,
                #aws_secret_access_key = aws_secret_key ,
                region_name = region[z],
    )

    client = boto3.client('ec2',
                #aws_access_key_id = aws_access_key ,
                #aws_secret_access_key = aws_secret_key ,
                region_name = region[z],
    )


    sg_id = []

    response = client.describe_security_groups()

    count3 = len(response['SecurityGroups'])

    for x in range(0,count3):
        if response['SecurityGroups'][x]['GroupName'] == group_name:
            sg_id.append(response['SecurityGroups'][x]['GroupId'])
        else:
            continue

    print(region[z])
    print(sg_id)


    count4 = len(sg_id)
    for x in range(0,count4):
        IpPermissions = []
        f = open(csv_name)
        csv_f = csv.reader(f)
        headers = next(csv_f)
        for row in csv_f:
                IpPermissions_loop={'IpProtocol': row[0],
                    'FromPort': int(row[1]),
                    'ToPort': int(row[2]),
                    'IpRanges': [{
                    'CidrIp': row[3], 
                    'Description': row[4]}]}

                IpPermissions.append(IpPermissions_loop) 

        sg_rule={'IpProtocol': '-1',
            'FromPort': -1,
            'ToPort': -1,
            'UserIdGroupPairs': [{
            'GroupId': sg_id[x],
            'Description': 'DevOps Linux base Security Group'}]}

        IpPermissions.append(sg_rule)
        security_group = ec2.SecurityGroup(sg_id[x])
        print(IpPermissions)
        try:
            security_group.revoke_ingress(IpPermissions=security_group.ip_permissions)
            data = security_group.authorize_ingress(
                IpPermissions=IpPermissions)
        except:
            print('no inbound rules in this region')
            data = security_group.authorize_ingress(
                IpPermissions=IpPermissions)


