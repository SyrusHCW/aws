import boto3
from botocore.exceptions import ClientError
import sys
import csv
import re

### User definedvars
region = 'us-east-2'
group_name = 'DOPS-WINDOWS-SG'
env_name = 'USE2-SB-LAB1'



#aws_access_key = sys.argv[1]
#aws_secret_key = sys.argv[2]

description = 'DevOps window instance security group'

csv_name = '{0}{1}'.format(group_name, '.csv')

ec2 = boto3.resource('ec2',
            #aws_access_key_id = aws_access_key ,
            #aws_secret_access_key = aws_secret_key ,
            region_name = region,
)

client = boto3.client('ec2',
            #aws_access_key_id = aws_access_key ,
            #aws_secret_access_key = aws_secret_key ,
            region_name = region,
)


vpc_name = '{0}{1}'.format(env_name, '-VPC')
vpc_id = []

response = client.describe_vpcs()

count0 = len(response['Vpcs'])

response['Vpcs'][1]['Tags'][0]['Key']


for x in range(0,count0):
    count1 = len(response['Vpcs'][x]['Tags'])
    #print(count1)
    for y in range(0,count1):
        if response['Vpcs'][x]['Tags'][y]['Key'] == 'Name' and response['Vpcs'][x]['Tags'][y]['Value'] == vpc_name:
            vpc_id.append(response['Vpcs'][x]['VpcId'])
        else:
            continue

vpc = ec2.Vpc(vpc_id[0])


sg_name = '{0}{1}'.format(env_name, group_name)

sg_id = []

response = client.describe_security_groups()

count3 = len(response['SecurityGroups'])


for x in range(0,count3):
    count4 = len(response['SecurityGroups'])
    if response['SecurityGroups'][x]['VpcId'] ==  vpc_id[0] and response['SecurityGroups'][x]['GroupName'] == group_name:
        sg_id.append(response['SecurityGroups'][x]['GroupId'])
        rules_count = len(response['SecurityGroups'][x]['IpPermissions'])
        print(rules_count)
        if rules_count > 0:
            security_group = ec2.SecurityGroup(sg_id[0])
            security_group.revoke_ingress(IpPermissions=security_group.ip_permissions)
            print(sg_id[0])
            print(True)
    else:
        continue


#print(sg_id)


pattern = re.compile("sg-")

group_name_id = []

for id in sg_id:  
    if pattern.search(sg_id[0]):
        group_name_id.append(sg_id[0])
        break
else:
    security_group = vpc.create_security_group(
            Description=description,
            GroupName=group_name,
            DryRun=False,
            )
    sg = str(security_group)
    group_name_id.append(sg[22:42])         


security_group = ec2.SecurityGroup(group_name_id)



count4 = len(group_name_id)
for x in range(0,count4):
    IpPermissions = []
    path = '{0}{1}'.format('security-groups/', csv_name)
    f = open(path)
    csv_f = csv.reader(f)
    headers = next(csv_f)
    print(csv_f)
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
        'GroupId': group_name_id[0],
        'Description': description}]}
    IpPermissions.append(sg_rule)
    security_group = ec2.SecurityGroup(group_name_id[0])
    print(IpPermissions)
    data = security_group.authorize_ingress(
        IpPermissions=IpPermissions)
    value = '{0}{1}{2}'.format(env_name, '-', group_name)
    tag = security_group.create_tags(
            DryRun=False,
            Tags=[
            {
                'Key': 'Name',
                'Value': value
            },
        ]
    )

